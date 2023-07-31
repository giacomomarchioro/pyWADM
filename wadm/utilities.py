from . import WADM
import json


def modify_WADM_json(path):
    """Modify an Web Annotation Data Model json file.
    This method parse only the frist level of the WADM object. All the nested
    object are left as dict.

    It is faster compared to read read_API3_json.

    Note:
        the method assumes the WADM object is complaint Web Annotation Data Model.

    Args:
        path (str): The path of the json file.
    """
    with open(path) as f:
        t = json.load(f)
    t.pop('@context')
    entitydict = {'Annotation': WADM.Annotation(),
                  'AnnotationCollection': WADM.AnnotationCollection(),
                  'AnnotationPage':WADM.AnnotationPage()}
    assert t['type'] in entitydict.keys(), "%s not a valid WADM object" % t['type']
    newobj = entitydict[t['type']]
    # TODO: find better solution .update will cause height and width to be set R.
    newobj.__dict__ = t
    return newobj


def read_API3_json_dict(jsondict, extensions=None, save_context=False):
    """Read an WADM json file complaint with Web Annotation Data Model.

    This method parse the major WADM types and map them to the WADM
    classes.

    Note:
        the method assumes the file is compliant with the Web Annotation Data
        model.

    Args:
        jsondict (dict): a dict representing the JSON file.
        extensions
    """

    jsondict.pop('@context')
    entitydict = {
     'Annotation': WADM.Annotation,
     'AnnotationPage': WADM.AnnotationPage,
     'FragmentSelector': WADM.FragmentSelector,
     'ImageApiSelector': WADM.ImageApiSelector,
     'PointSelector': WADM.PointSelector,
     'SpecificResource': WADM.SpecificResource,
     'SvgSelector': WADM.SvgSelector,
     'TextPositionSelector':WADM.TextPositionSelector,
     'XPathSelector':WADM.XPathSelector,
     'CssSelector':WADM.CssSelector,
     'Software':WADM.Software,
     'Organization':WADM.Organization,
     'Person':WADM.Person,
     'RangeSelector':WADM.RangeSelector,
     'TextQuoteSelector':WADM.TextQuoteSelector,

        }
    assert jsondict['type'] in entitydict.keys(), "%s not a valid IIIF object" % jsondict['type']

    def map_to_class(obj, iscollection=False):
        parent_is_collection = False
        if obj['type'] == 'Collection':
            parent_is_collection = True
        if 'items' in obj.keys():
            for n, item in enumerate(obj['items']):
                obj['items'][n] = map_to_class(item, iscollection=parent_is_collection)
        # we can map directly to each class using the object type except for
        # manifest References which as the same type of Manifest
        if iscollection and obj['type'] == "Manifest" and 'items' not in obj.items():
            newobj = iiifpapi3.refManifest()
        else:
            newobj = entitydict[obj['type']]()
        # TODO: find better solution .update will cause height and width to be set R.
        # newobj.__dict__ = newobj works apparently with no problem
        newobj.__dict__.update(obj)
        # Specific cases
        if obj['type'] == 'Canvas':
            if newobj.duration is not None:
                newobj.set_duration(newobj.duration)
        return newobj
    newobj = map_to_class(jsondict)
    return newobj


def read_WADM_json(path, extensions=None, save_context=False):
    """Read an WADM json file complaint with Web Annotation Data Model and map 
    the WADM types to classes.

    This method parse the major WADM types and map them to the WADM
    classes.

    Note:
        the method assumes the IIIF object is complaint to API 3.0.

    Args:
        path (str): path of the jsonfile
    """
    with open(path) as f:
        jsondict = json.load(f)
    return read_API3_json_dict(jsondict, extensions=extensions, save_context=save_context)


def read_WADM_json_file(path, extensions=None, save_context=False):
    """Read an WADM json file complaint with Web Annotation Data Model and map
    the WADM types to classes.

    This method parse the major WADM types and map them to the WADM
    classes.
    NOTE: the method assumes the WADM object is complaint Web Annotation Data
    Model.

    Args:
        path (str): path of the jsonfile
    """
    with open(path) as f:
        jsondict = json.load(f)
    return read_API3_json_dict(jsondict, extensions=extensions, save_context=save_context)


def delete_object_byID(obj, id):
    """Deletes nested WADM objects using the ID.

    Args:
        obj (dict): a dict representing the WADM object.
        id (str): the ID of the object to be delete.

    Returns:
        True: if the ID was found.
    """
    if hasattr(obj, "__dict__"):
        obj = obj.__dict__
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'id' and value == id:
                return True
            delete_object_byID(value, id)
    if isinstance(obj, list):
        for item in obj:
            if delete_object_byID(item, id):
                obj.remove(item)
    else:
        pass


def remove_and_insert_new(obj, id, newobj):
    """Remove inplace from any WADM object (Annotation, AnnotationPage,  etc)
    the object with the given id and insert the new object.

    Args:
        obj (WADMobject): The object to modify.
        id (str): The id of the object to remove.
        newobj (WADMobject): The new object to insert.

    Returns:
        counter (int): The number of objects removed. If 0, nothing was removed.
    """
    def remove_and_insert_new_rec(obj, id, newobj):
        nonlocal counter
        if hasattr(obj, "__dict__"):
            obj = obj.__dict__
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'id' and value == id:
                    counter += 1
                    return True
                remove_and_insert_new_rec(value, id, newobj)
        if isinstance(obj, list):
            for item in obj:
                if remove_and_insert_new_rec(item, id, newobj):
                    obj.remove(item)
                    obj.append(newobj)
        else:
            pass
    counter = 0
    remove_and_insert_new_rec(obj, id, newobj)
    return counter