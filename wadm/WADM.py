"""Implementation of Web Annotation Data Model.

This is a Python module built for easing the construction of JSON object
compliant with the Web Annotation Data Model.

Example:
    >>> from wadm import WADM
    >>> anno = WADM.Annotation()
    >>> anno.set_id("http://example.org/anno1")
    >>> anno.set_body("http://example.org/post1")
    >>> anno.set_target("http://example.com/page1")
    >>> anno.to_json()

Attributes:
    BASE_URL (str): Module level variable containing the URL to be preappend
        to iiifpapi3._CoreAttributes.set_id extend_baseurl

    LANGUAGES (list[str]): Module level variable containing a list of accepted
        languages. This variable is used for checking accepted languages, using
        the `IANA sub tag registry`_

    CONTEXT (str,list): Module level variable containing the context of the
        JSONLD file. Can be set to a list in case of multiple contexts.

    INVALID_URI_CHARACTERS (str): A list of characters that are not accepted
        in the URL.


Warning:
    only language subtags are checked not variants or composite strings.
    You can manually add a language if you need to use subtags:

Example:
    >>> from WADM import BCP47lang
    >>> WADM.LANGUAGES.append("de-DE-u-co-phonebk")

Todo:
    * The motivation of the Annotations must not be painting, and the target of
      the Annotations must include this resource or part of it
    * Annotations that do not have the motivation value painting must not be in
      pages referenced in items, but instead in the annotations property.
    * You have to also use ``sphinx.ext.todo`` extension

.. _IANA sub tag registry:
    https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
"""
from . import visualization_html
from .BCP47_tags_list import lang_tags
from .dictmediatype import mediatypedict
import json
import warnings
import copy
import re
global BASE_URL
BASE_URL = "https://"
global LANGUAGES
LANGUAGES = lang_tags
global MEDIATYPES
MEDIATYPES = mediatypedict
global CONTEXT
CONTEXT = "http://www.w3.org/ns/anno.jsonld"
global INVALID_URI_CHARACTERS
# removed comma which is used by WADM Image API and #
INVALID_URI_CHARACTERS = r"""!"$%&'()*+ :;<=>?@[\]^`{|}~ """
TYPES = ["Text","Video","Sound","Image","Dataset"]

class Required(object):
    """HELPER CLASS

    Note:
        This is not an WADM object but a class used by this software to
        identify required fields. This is equivalent to MUST statement in the
        guideline with the meaning of https://tools.ietf.org/html/rfc2119 .
    """

    def __init__(self, description=None):
        self.Required = description

    def __eq__(self, o):
        return True if isinstance(o, self.__class__) else False

    def __repr__(self):
        return 'Required attribute:%s' % self.Required


class Recommended(object):
    """HELPER CLASS

    Note:
        This is not an WADM object but a class used by this software to
        identify recommended fields. This is equivalent to SHOULD statement in
        the guideline with the meaning of https://tools.ietf.org/html/rfc2119.
    """

    def __init__(self, description=None):
        self.Recommended = description

    def __eq__(self, o):
        return True if isinstance(o, self.__class__) else False

    def __repr__(self):
        return 'Recommended attribute:%s' % self.Recommended


# Note: we use None for OPTIONAL with the meaning of
# https://tools.ietf.org/html/rfc2119

# The package is based on 4 main helper functions:

def unused(attr):
    """This function checks if an attribute is not set (has no value in it).
    """
    if isinstance(attr, (Required, Recommended)) or attr is None:
        return True
    else:
        return False


# For performance optimization we can reduce the instantiation of Classes
if not __debug__:
    def Recommended(msg=None):
        return None

    def Required(msg=None):
        return None

    def unused(attr):
        return True if attr is None else False


def serializable(attr):
    """Check if attribute is Required and if so rise Value error.

    Args:
        attr : the value of the dictionary of the attribute of the instance.
    """
    if isinstance(attr, Required):
        raise ValueError(attr)
    if isinstance(attr, Recommended) or attr is None:
        return False
    else:
        return True


def add_to(selfx, destination, classx, obj, acceptedclasses=None, target=None):
    """Helper function used for adding WADM object to to WADM lists.

    Args:
        selfx (object): The class it-self
        destination (str): The class list attribute where the object will be stored.
        classx (object): The WADM class that will be used for instantiating the
            obejct.
        obj (object): An already instantiated WADM object.
        acceptedclasses (objects, optional): Accepted classes for obj. Defaults to None.
        target (str, optional): The target of an Annotation. Defaults to None.

    Raises:
        ValueError: When users try to add the wrong object to a list.

    Returns:
        WADM object: A reference to an instance of the WADM object.
    """
    # if the argument is none we create a list.
    if unused(selfx.__dict__[destination]):
        selfx.__dict__[destination] = []
    # if there is already a valid string we insert it on the list.
    elif not isinstance(selfx.__dict__[destination],list):
        selfx.__dict__[destination] = [selfx.__dict__[destination]]
    # if we are not providing a WADM Object we create one.
    if obj is None and target is None:
        obj = classx()
        selfx.__dict__[destination].append(obj)
        return obj
    elif obj is None:
        # used for annotation.
        obj = classx(target=target)
        selfx.__dict__[destination].append(obj)
        return obj
    # otherwise we check that the object that we provide has the right type.
    else:
        if acceptedclasses is None:
            acceptedclasses = classx
        if isinstance(obj, acceptedclasses):
            selfx.__dict__[destination].append(obj)
        else:
            obj_name = obj.__class__.__name__
            class_name = selfx.__class__.__name__
            raise ValueError("%s object cannot be added to %s." %
                             (obj_name, class_name))


def addOrSet_to(selfx, destination, classx, obj, acceptedclasses=None, target=None):
    """Helper function used for adding WADM object to to WADM lists.

    Args:
        selfx (object): The class it-self
        destination (str): The class list attribute where the object will be stored.
        classx (object): The WADM class that will be used for instantiating the
            obejct.
        obj (object): An already instantiated WADM object.
        acceptedclasses (objects, optional): Accepted classes for obj. Defaults to None.
        target (str, optional): The target of an Annotation. Defaults to None.

    Raises:
        ValueError: When users try to add the wrong object to a list.

    Returns:
        WADM object: A reference to an instance of the WADM object.
    """
    # we check if we provide an object and if so has the correct type
    if obj is None and target is None:
        obj = classx()
    elif obj is None:
        # used for annotation.
        obj = classx(target=target)
    else:
        if acceptedclasses is not None:
            assert isinstance(obj,acceptedclasses)
    # we check where to put the object.
    if unused(selfx.__dict__[destination]):
        selfx.__dict__[destination] = obj
    # if there is already something we insert it on the list.
    elif not isinstance(selfx.__dict__[destination],list):
        selfx.__dict__[destination] = [selfx.__dict__[destination]]
        selfx.__dict__[destination].append(obj)
    # otherwise we just inserted in the list.
    else:
        selfx.__dict__[destination].append(obj)
    return obj

def setOrAppendStr(selfx,destination,value,acceptedObj):
    if unused(selfx.__dict__[destination]):
        selfx.__dict__[destination] = value
    # if there is already a valid string we insert it on the list.
    elif isinstance(selfx.__dict__[destination],str):
        selfx.__dict__[destination] = [selfx.__dict__[destination]]
        selfx.__dict__[destination].append(value)
    # if there is already a valid object we insert it on the list
    elif isinstance(selfx.__dict__[destination],acceptedObj):
        selfx.__dict__[destination] = [selfx.__dict__[destination]]
        selfx.__dict__[destination].append(value)
    # if there is already a list we just append
    elif isinstance(selfx.__dict__[destination],list):
        selfx.__dict__[destination].append(value)
    else:
        raise ValueError(f"Could not add {value} to {destination}.")

def check_valid_URI(URI):
    """Check if it is a valid URI.

    Args:
        URI (str): The URI to check.

    Returns:
        Bool: True if it is valid.
    """
    isvalid = True
    URI = URI.replace("https:/", "", 1)
    URI = URI.replace("http:/", "", 1)
    # we remove the selector.
    URI = re.sub(r'#xywh=\d+?,\d+?,\d+?,\d+?$', '', URI)
    URI = re.sub(r'#xywh=pct:\d+?,\d+?,\d+?,\d+?$', '', URI)
    for indx, carat in enumerate(URI):
        if carat in INVALID_URI_CHARACTERS:
            if carat == " ":
                carat = "a space"
            arrow = " "*(indx) + "^"
            isvalid = False
            print("I found: %s here. \n%s\n%s" % (carat, URI, arrow))
    return isvalid


def check_ID(extendbase_url, objid):
    """Function for creating and checking IDs.

    Args:
        extendbase_url (str): The baseURL to extend.
        objid (str): A valid ID.

    Raises:
        ValueError: When trying to use both args together.
    """
    if extendbase_url:
        if objid:
            raise ValueError(
                "Set id using extendbase_url or objid not both.")
        # this prevents the case the user forget the slash; in case the user
        # really wants to join the string: objid = iiifpapi3.BASE_URL + myid
        assert BASE_URL.endswith("/") or extendbase_url.startswith("/"), \
            "Add / to extandbase_url or BASE_URL"
        joined = "".join((BASE_URL, extendbase_url))
        assert joined.startswith("http"), "ID must start with http or https"
        assert check_valid_URI(joined), "Special characters must be encoded"
        return joined
    else:
        assert objid.startswith("http"), "ID must start with http or https"
        assert check_valid_URI(objid), "Special characters must be encoded"
        return objid

class _Format(object):
    """HELPER CLASS for setting the Format.
    """
    def set_format(self, format):
        """Set the format of the resource.

        https://iiif.io/api/presentation/3.0/#format

        WADM: The specific media type (often called a MIME type) for a content
        resource, for example image/jpeg. This is important for distinguishing
        different formats of the same overall type of resource, such as
        distinguishing text in XML from plain text.

        Args:
            format (str): Usually  is the MIME e.g. image/jpeg.
        """

        assert "/" in format, "Format should be in the form type/format e.g. image/jpeg"
        assert format.split("/")[0].isalpha(), "Format should be in the form type/format e.g. image/jpeg"
        assert not format == 'image/jpg', "Correct media type for jpeg should be image/jpeg not image/jpg"
        assert not format == 'image/tif', "Correct media type  for tiff should be image/tiff"
        assert any(format in sl for sl in MEDIATYPES.values()), "Not a IANA valid media type."
        self.format = format

    def add_format(self, format):
        """Set the format of the resource.

        https://iiif.io/api/presentation/3.0/#format

        WADM: The specific media type (often called a MIME type) for a content
        resource, for example image/jpeg. This is important for distinguishing
        different formats of the same overall type of resource, such as
        distinguishing text in XML from plain text.

        Args:
            format (str): Usually  is the MIME e.g. image/jpeg.
        """
        if unused(self.format):
            self.format = []
        elif isinstance(self.format,str):
            self.format = [self.format]
        assert "/" in format, "Format should be in the form type/format e.g. image/jpeg"
        assert format.split("/")[0].isalpha(), "Format should be in the form type/format e.g. image/jpeg"
        assert not format == 'image/jpg', "Correct media type for jpeg should be image/jpeg not image/jpg"
        assert not format == 'image/tif', "Correct media type  for tiff should be image/tiff"
        assert any(format in sl for sl in MEDIATYPES.values()), "Not a IANA valid media type."
        self.format.append(format)

def checkDatetime(datetime):
    # check using a modified regex from www.w3.org
        # https://www.w3.org/TR/xmlschema11-2/#dateTime
    r = (r"-?([1-9][0-9]{3,}|0[0-9]{3})"
        r"-(0[1-9]|1[0-2])"
        r"-(0[1-9]|[12][0-9]|3[01])"
        r"T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))"
        r"(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))")
    assert re.match(r, datetime), "The value must be an XSD dateTime"\
        "literal with a timezone. It was: %s" % datetime
    if datetime[-1] != "Z":
        warnings.warn(f"The value should be given in UTC with the Z was {datetime}")
    return datetime

# Let's group all the common arguments across the different types of collection
class _CoreAttributes(object):
    """HELPER CLASS

    The core attributes are: ID, Type

    ID an type attributes are required. The other might vary.
    """

    def __init__(self):
        super(_CoreAttributes, self).__init__()
        self.id = Required(
            "A %s must have the ID property." %
            self.__class__.__name__)
        self.type = self.__class__.__name__
        # These might be suggested or may be used if needed.

    def set_id(self, objid=None, extendbase_url=None):
        """Set the ID of the object

        WADM: The URI that identifies the resource. If the resource is only
        available embedded within another resource (see the terminology section
        for an explanation of “embedded”), such as a Range within a Manifest,
        then the URI may be the URI of the embedding resource with a unique
        fragment on the end. This is not true for Canvases, which must have
        their own URI without a fragment.

        Args:
            objid (str, optional): A string corresponding to the ID of the
                object `id = objid`.Defaults to None.
            extendbase_url (str , optional): A string containing the URL part
                to be joined with the iiifpapi3.BASE_URL:
                `id = iiifpapi3.BASE_URL + extendbase_url`. Defaults to None.
        """
        self.id = check_ID(extendbase_url, objid)

    def json_dumps(
            self,
            dumps_errors=False,
            ensure_ascii=False,
            sort_keys=False,
            context=None):
        """Dumps the content of the object in JSON format.

        Args:
            dumps_errors (bool, optional): If set true it shows any problem
                found directly on the JSON file with a Required or Recommended
                tag.Defaults to False.
            ensure_ascii (bool, optional): Ensure ASCI are used.
                Defaults to False.
            sort_keys (bool, optional): Sort the keys. Defaults to False.
            context (str,list, optional): Add additional context. Defaults to
                None.

        Returns:
            str: The JSON object as a string.
        """
        if context is None:
            context = CONTEXT

        if not __debug__:
            # in debug Required and Recommend are None hence we use a faster
            # serializer
            print("Debug False")
            dumps_errors = True

        def serializerwitherrors(obj):
            return {k: v for k, v in obj.__dict__.items() if v is not None}

        def serializer(obj):
            return {k: v for k, v in obj.__dict__.items() if serializable(v)}
        if dumps_errors:
            res = json.dumps(
                self,
                default=serializerwitherrors,
                indent=2,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys)
        else:
            res = json.dumps(
                self,
                default=serializer,
                indent=2,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys)
        # little hack for fixing context first 3 chrs "{\n"
        res = "".join(('{\n  "@context": %s,\n ' % json.dumps(context), res[3:]))
        return res

    def orjson_dumps(
            self,
            dumps_errors=False,
            context=None):
        """Dumps the content of the object in JSON format using orJSON library.

        Args:
            dumps_errors (bool, optional): If set true it shows any problem
                found, directly on the JSON file with a Required or Recommended
                tag.Defaults to False.
            ensure_ascii (bool, optional): Ensure ASCI are used.
                Defaults to False.
            sort_keys (bool, optional): Sort the keys. Defaults to False.
            context (str,list, optional): Add additional context. Defaults to None.

        Returns:
            str: The JSON object as a string.
        """
        import orjson
        if context is None:
            context = CONTEXT

        if not __debug__:
            # in debug Required and Recommend are None hence we use a faster
            # serializer
            print("Debug False")
            dumps_errors = True

        def serializerwitherrors(obj):
            return {k: v for k, v in obj.__dict__.items() if v is not None}

        def serializer(obj):
            return {k: v for k, v in obj.__dict__.items() if serializable(v)}

        if dumps_errors:
            res = orjson.dumps(
                self,
                default=serializerwitherrors,
                option=orjson.OPT_INDENT_2)
        else:
            res = orjson.dumps(
                self,
                default=serializer,
                option=orjson.OPT_INDENT_2)
        # little hack for fixing context first 3 chrs "{\n"
        res = "".join(('{\n  "@context": %s,\n ' % json.dumps(context),
                      res[3:].decode("utf-8")))
        return res

    def to_json(
            self,
            dumps_errors=False,
            ensure_ascii=False,
            sort_keys=False,
            context=None):
        """Return the object with the JSON syntax.

        Args:
            filename (str): The filename.
            save_errors (bool, optional): If True also the errors will be
                dumped. Defaults to False.
            ensure_ascii (bool, optional): If True only ASCI character will be
                used. Defaults to False.
            context (str,list, optional): Add additional contexts to the JSON.
                Defaults to None.
        Return:
            dict: a JSON dump of the object as dict.
        """
        res = json.loads(self.json_dumps(
            dumps_errors=dumps_errors,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys,
            context=context))
        return res

    def json_save(self, filename, save_errors=False, ensure_ascii=False, context=None):
        """Save the JSON object to file.

        Args:
            filename (str): The filename.
            save_errors (bool, optional): If True also the errors will be
                dumped. Defaults to False.
            ensure_ascii (bool, optional): If True only ASCI character will be
                used. Defaults to False.
            context (str,list, optional): Add additional contexts to the JSON.
                Defaults to None.
        """
        with open(filename, 'w') as f:
            f.write(self.json_dumps(
                dumps_errors=save_errors, ensure_ascii=ensure_ascii, context=context))

    def orjson_save(self, filename, save_errors=False, context=None):
        """Save the JSON object to file.

        Args:
            filename (str): The filename.
            save_errors (bool, optional): If True also the errors will be
                dumped. Defaults to False.
            ensure_ascii (bool, optional): If True only ASCI character will be
                used. Defaults to False.
            context (str,list, optional): Add additional contexts to the JSON.
                Defaults to None.
        """
        with open(filename, 'w') as f:
            f.write(self.orjson_dumps(
                dumps_errors=save_errors, context=context))

    def inspect(self):
        """Print the object in the derminal and show the missing required
        and recomended fields.

        Returns:
            bool: True.
        """
        jdump = self.json_dumps(dumps_errors=True)
        print(jdump)
        print("Missing required field: %s." % jdump.count('"Required":'))
        print("Missing recommended field: %s." % jdump.count('"Recommended":'))
        return True

    def show_errors_in_browser(self, getHTML=False):
        """Opens a browser window showing the required and the reccomended
        attributes.

        Args:
            getHTML (bool, optional): Returns the HTML to a variable.
            Defaults to False.

        Returns:
            str: If getHTML is set to true returns the HTML as str.
        """
        jsonf = self.json_dumps(dumps_errors=True)
        HTML = visualization_html.show_error_in_browser(jsonf, getHTML=getHTML)
        return HTML

    def __repr__(self):
        if unused(self.id):
            id_ = "Missing"
        else:
            id_ = self.id
        if unused(self.type):
            type_ = "Type Missing"
        else:
            type_ = self.type
        return " id:".join((type_, id_))


class _ImmutableType(object):
    """HELPER CLASS In some WADM objects the type cannot be changed.
    """
    def set_type(self, mtype=None):
        """In case of WADM objects with predefined type this function won't
        change the type but will rise an error if you try to change it.

        https://iiif.io/api/presentation/3.0/#type

        Args:
            mtype (str, optional): the type of the object.
                Defaults to None.

        Raises:
            ValueError: In case _you are trying to set a type.
        """
        cnm = self.__class__.__name__
        cty = self.type
        if mtype == cty or mtype is None:
            m = "%s type is by default %s, this set will be ingored." % (cnm, cty)
            warnings.warn(m)
        else:
            e = "The %s type must be set to '%s' was: %s " % (cnm, cty, mtype)
            raise ValueError(e)

class _Agent(_CoreAttributes):
    """Agents

    W3C:
    More information about the agents involved in the creation of an Annotation
    is normally required beyond an IRI that identifies them. This includes
    whether they are an individual, a group or a piece of software and
    properties such as real name, account nickname, and email address.

    Example Use Case: Kelly wants to submit an Annotation to a system that does
    not manage her identity, and would like a pseudonym to be displayed.
    Her client adds this information to the Annotation to send to the service.

    """
    def set_type(self,type):
        """The agent type.

        Args:
            type (str): The Agent type (Person,Organization,Software)
        """
        assert type in ["Person","Organization","Software"], "Type must be Person, Organization or Software."
        self.type = type

    def set_name(self,name):
        """Set the name of the agent.

        Each agent should have exactly 1 name property, and may have 0 or more.

        Args:
            name (str): The name of the agent.
        """
        self.name = name

    def set_nickname(self,nickname):
        """Set the nickname of the agent.

        Each agent should have exactly 1 nickname property, and may have 0.

        Args:
            nickname (str): The nickname of the agent.
        """
        self.nickname = nickname

    def set_email(self,email):
        """Set the email of the agent.

        Each agent should have exactly 1 nickname property, and may have 0.

        Args:
            email (str): The email of the agent.
        """
        self.email = email

    def set_email_sha1(self,email_sha1):
        """Set the email_sha1 of the agent.

        The text representation of the result of applying the sha1 algorithm to
        the email IRI of the agent,including the 'mailto:' prefix and no 
        whitespace. This allows the mail address to be used as an identifier 
        without publishing the address publicly.

        Args:
            email (str): The email of the agent.
        """
        self.email_sha1 = email_sha1

    def set_homepage(self,homepageUrl):
        assert check_valid_URI(homepageUrl),f"Invalid URI for homepage: {homepageUrl}"
        self.homepage = homepageUrl

class _Selector(_ImmutableType):
    def __init__(self):
        self.type = self.__class__.__name__
        self.refinedBy = None

    def add_refinedBy(self,selector):
        assert isinstance(selector,_Selector),"Selector must be a valid selector"
        if self.refinedBy is None:
           self.refinedBy = selector
        # if there is already a valid object we insert it on the list.
        elif isinstance(self.refinedBy,_Selector):
            self.refinedBy = [self.refinedBy]
            self.refinedBy.append(selector)
        # if there is already a list we just append
        elif isinstance(self.refinedBy,list):
            self.refinedBy.append(selector)
        return selector


class ImageApiSelector(_Format,_Selector):
    """IIIF Resource

    https://iiif.io/api/annex/openannotation/#iiif-image-api-selector

    IIIF: The Image API Selector is used to describe the operations available
    via the Image API in order to retrieve a particular image representation.
    In this case the resource is the abstract image as identified by the IIIF
    Image API base URI plus identifier, and the retrieval process involves
    adding the correct parameters after that base URI. For example, the top
    left hand quadrant of an image has the region parameter of pct:0,0,50,50
    which must be put into the requested URI to obtain the appropriate
    representation.
    """
    def __init__(self):
        self.type = "ImageApiSelector"
        self.region = None
        self.size = None
        self.rotation = None
        self.quality = None
        self.fromat = None

    def set_region(self, region):
        """Set the region of the image API selector.

        Args:
            region (str): The region of the ImageAPI selector.
        """
        self.region = region

    def set_rotation(self, rotation):
        """Set the rotation of the image API selector.

        Args:
            rotation (str,int): The rotation to be applied to the image.
        """
        self.rotation = rotation

    def set_quality(self, quality):
        """Set the quality to to the ImageAPI  selector.

        Args:
            quality (str): e.g. default
        """
        self.quality = quality

    def set_size(self, size):
        """Set the size parameter of the ImageAPI selector.

        Args:
            size (str): The requested size of the image.
        """
        self.size = size


class PointSelector(_Selector):
    """

    https://iiif.io/api/annex/openannotation/#point-selector

    There are common use cases in which a point, rather than a range or area,
    is the target of the Annotation. For example, putting a pin in a map should
    result in an exact point, not a very small rectangle. Points in time are
    not very short durations, and user interfaces should also treat these
    differently. This is particularly important when zooming in (either
    spatially or temporally) beyond the scale of the frame of reference. Even
    if the point takes up a 10 by 10 pixel square at the user’s current
    resolution, it is not a rectangle bounding an area.

    It is not possible to select a point using URI Fragments with the Media
    Fragment specification, as zero-sized fragments are not allowed. In order
    to fulfill the use cases, this specification defines a new Selector class
    called PointSelector.

    Property	Description
    type	Required. Must be the value “PointSelector”.
    x	Optional. An integer giving the x coordinate of the point, relative to
        the dimensions of the target resource.
    y	Optional. An integer giving the y coordinate of the point, relative to
        the dimensions of the target resource.
    t	Optional. A floating point number giving the time of the point in seconds,
        relative to the duration of the target resource
    """

    def __init__(self):
        self.type = self.__class__.__name__
        self.x = None
        self.y = None
        self.t = None

    def set_x(self, x):
        """Set the x coordinate.

        Args:
            x (int): The x coordinate.
        """
        self.x = x

    def set_y(self, y):
        """Set the y coordiante.

        Args:
            y (int): The y coordinate.
        """
        self.y = y

    def set_t(self, t):
        """Set the time time of the point in seconds.

        Args:
            t (float): The time of the point in seconds relative to the duration.
        """
        self.t = t


class FragmentSelector(_Selector):
    """
    W3C: As the most well understood mechanism for selecting a Segment is to
    use the fragment part of an IRI defined by the representation's media type,
    it is useful to allow this as a description mechanism via a Selector.

    https://www.w3.org/TR/annotation-model/#fragment-selector

    """
    def __init__(self):
        super(FragmentSelector,self).__init__()
        self.value = Required("A fragment selector must have a value!")
        self.conformsTo = Recommended("The Fragment Selector should have exactly 1 conformsTo link to the specification that defines the syntax of the fragment")

    def set_value(self, value):
        """Set the value of the FragmentSelector

        Args:
            value (int): The
        """
        self.value = value

    def set_xywh(self, x, y, w, h):
        """Set the starting x and y point and the widht and height.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
            w (int): The width coordinate.
            h (int): The hieght coordinate.
        """
        self.value = "xywh=%i,%i,%i,%i" % (x, y, w, h)

    def set_conformsTo(self,fragmentSpecification):
        self.conformsTo = fragmentSpecification


class SvgSelector(_Selector):
    """The SvgSelector is used to select a non rectangualar region of an image.
    https://www.w3.org/TR/annotation-model/#svg-selector
    """
    def __init__(self):
        super(SvgSelector,self).__init__()
        self.value = None

    def set_value(self, value):
        """Set the value of the SVG Selector

        Args:
            value (str): A string containing the SVG element.
        """
        self.value = value

class CssSelector(_Selector):
    def __init__(self) -> None:
        super(CssSelector,self).__init__()
        self.value = None

    def set_value(self,value):
        self.value = value

class XPathSelector(_Selector):
    def __init__(self) -> None:
        super(XPathSelector,self).__init__()
        self.value = None

    def set_value(self,value):
        self.value = value

class TextPositionSelector(_Selector):
    def __init__(self) -> None:
        super(TextPositionSelector,self).__init__()
        self.start = None
        self.end = None

    def set_end(self,end):
        """The end position of the segment of text. The character is not 
        included within the segment.

        Args:
            end (int,str): The end position of the segment of text.

        """
        self.end = int(end)

    def set_start(self,start):
        """The starting position of the segment of text. The first character in
        the full text is character position 0, and the character is included
        within the segment.

        Args:
            start (int,str): The starting position of the segment of text.
        """
        self.start = int(start)

class DataPositionSelector(_Selector):
    def __init__(self) -> None:
        super(DataPositionSelector,self).__init__()
        self.start = None
        self.end = None

    def set_end(self,end):
        """The end position of the segment of data.
        The last character is not included within the segment.

        Args:
            end (int,str): The end position of the segment of data. The last
            character is not included within the segment.

        """
        self.end = int(end)

    def set_start(self,start):
        """The starting position of the segment of data.
        The first byte is character position 0.

        Args:
            start (int,str): The starting position of the segment of data.
            The first byte is character position 0.
        """
        self.start = int(start)

class TextQuoteSelector(_Selector):
    def __init__(self) -> None:
        super(TextQuoteSelector,self).__init__()
        self.exact = None
        self.prefix = None
        self.suffix = None

    def set_exact(self,exact):
        """A copy of the text which is being selected, after normalization.


        Args:
            exact (str): The text which is being selected, after normalization.

        """
        self.exact = exact

    def set_prefix(self,prefix):
        """A snippet of text that occurs immediately before the text which is
        being selected.

        Args:
            prefix (str): A snippet of text that occurs immediately before the text which is being selected.
        """
        self.prefix = prefix

    def set_suffix(self,suffix):
        """The snippet of text that occurs immediately after the text which is
        being selected.
        Each TextQuoteSelector should have exactly 1 suffix property, and must
        not have more than 1.

        Args:
            suffix (str): The snippet of text that occurs immediately after the
            text which is being selected.
        """
        self.suffix = suffix

class RangeSelector(_Selector):
    def __init__(self) -> None:
        super(RangeSelector,self).__init__()
        self.startSelector = None
        self.endSelector = None

    def set_startSelector(self,startSelector):
        self.startSelector = startSelector

    def set_endSelector(self,endSelector):
        self.endSelector = endSelector

class _SetSelector(object):
    def set_selector(self, selector):
        """Set the selector of the specifc resource.

        Args:
            selector (any): The selector of the specific resource.
        """
        self.selector = selector

class _RightsInformationIdentities(object):
    """3.3.6 Rights Information"""
    def __init__(self):
        super(_RightsInformationIdentities, self).__init__()
        self.rights = None
        self.via = None

    def add_rights(self,rights):
        assert check_valid_URI(rights),"The value must be an IRI."
        if unused(self.rights):
            self.rights = rights
        elif isinstance(self.rights,str):
            self.rights = [self.rights]
            self.rights.append(rights)

    def set_canonical(self,canonical):
        self.canonical = canonical

    def add_via(self,via):
        assert check_valid_URI(via),"The value must be an IRI."
        setOrAppendStr(self,"via",via,str)

class Person(_Agent,_ImmutableType):
    """The class for a human agent.
    """
    def __init__(self):
        super(_Agent, self).__init__()
        self.type = "Person"

class Organization(_Agent,_ImmutableType):
    """The class for an organization, as opposed to an individual.
    """
    def __init__(self):
        super(_Agent, self).__init__()
        self.type = "Organization"

class Software(_Agent,_CoreAttributes,_ImmutableType):
    def __init__(self):
        super(Software, self).__init__()

    def set_softwareVersion(self,softwareVersione):
        setattr(self,"schema:softwareVersion",softwareVersione)

class _LifeCycleInformation(object):

    def __init__(self):
        super(_LifeCycleInformation, self).__init__()
        self.creator = None
        self.generator = None

    def set_creator(self,creator=None):
        if creator is None:
            self.creator = _Agent()
        if issubclass(type(creator),(str,_Agent)):
            self.creator = creator
        return self.creator

    def add_creator(self,creatorObj=None):
        return add_to(self, 'creator', _Agent, creatorObj, (_Agent, str))

    def set_generator(self,generator=None):
        if generator is None:
            self.generator = _Agent()
        if issubclass(type(generator),(str,_Agent)):
            self.generator = generator
        return self.generator

    def add_generator(self,generatorObj):
        return add_to(self, 'generator', _Agent, generatorObj, (_Agent, str))

    def set_created(self,datetime):
        self.created = checkDatetime(datetime=datetime)

    def set_generated(self,datetime):
        """Set the time at which the Annotation serialization was generated.

        Args:
            datetime (str): The time at which the Annotation serialization was 
            generated.
        """
        self.generated = checkDatetime(datetime=datetime)

    def set_modified(self,datetime):
        """Set the time at which the resource was modified, after creation.

        Args:
            datetime (str): The time at which the resource was modified, after
            creation.
        """
        self.modified = checkDatetime(datetime=datetime)

    def set_created(self,datetime):
        """Set the time at which the resource was created.

        Args:
            datetime (str): The time at which the resource was created.
        """
        self.created = checkDatetime(datetime=datetime)

class _IntendedAudience(_CoreAttributes):
    def __init__(self):
        super(_IntendedAudience,self).__init__()
        self.type = Recommended("The Audience should have 1 or more types and they should come from the schema.org class structure.")

    def set_type(self,mtype):
        assert mtype.startswith("schema:"), "First part should start with schema: prefix"
        self.type = mtype

    def add_type(self,mtype):
        assert mtype.startswith("schema:"), "First part should start with schema: prefix"
        if unused(self.type):
            self.type = []
        elif isinstance(self.type,str):
            self.type = [self.type]
        self.type.append(mtype)

    def add_schemaProperty(self,property,value):
        assert property.startswith("schema:"), "First part should start with schema: prefix"
        setattr(self,property,value)

# Common helpers methods that will be used for constructing the WADM objects.

class _AddLanguage(object):
    """HELPER CLASS for adding languages.
    """
    def add_language(self, language):
        """add a language to the language list of the resource.

        https://iiif.io/api/presentation/3.0/#language-of-property-values

        Example:
            >>> manifest.add_language('en')

        Note:
            pyWADM accept only single tag, in case you need subtags you
            need to add them to iiifpapi3.LANGUAGES::

            >>> from WADM import BCP47lang
            >>> WADM.LANGUAGES.append("de-DE-u-co-phonebk")

        Args:
            language (str): A BCP 47 language tag e.g. en, it, es.
        """
        assert language in LANGUAGES or language == "none", \
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        setOrAppendStr(self,'language',language,str)

class _Source(object):

    def set_source(self, source=None, extendbase_url=None):
        """Set the source of the SpecificResource

        Args:
            source (str): The source is usually an URL.
            extendbase_url (str, optional): For extending the BASE_URL and
                using it as a source. Defaults to None.
        """
        assert isinstance(source,(str,_BodiesAndTargets,type(None))), "Must be a valid source class or none"
        if isinstance(source,str):
            self.source = check_ID(extendbase_url=extendbase_url, objid=source)
        elif isinstance(source,_BodiesAndTargets):
            self.source = source
        elif source is None:
            self.source = _BodiesAndTargets()
        self.id = Recommended("In case of Source we set it recommend. not sure.")
        return self.source
class _BodiesAndTargets(_CoreAttributes,_Format,_AddLanguage,
                        _LifeCycleInformation,_RightsInformationIdentities,
                        _Source,_SetSelector):
    def __init__(self, target=Required()):
        super(_BodiesAndTargets, self).__init__()
        self.type = None
        self.format = Recommended("It should have at least one format")
        self.processingLanguage = Recommended("It should have one language")
        self.language = Recommended("It should have one language")
        self.textDirection = None
        self.accessibility = None
        self.source = None

    def set_processingLanguage(self,language):
        assert language in LANGUAGES or language == "none",\
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        self.processingLanguage = language

    def set_language    (self,language):
        assert language in LANGUAGES or language == "none",\
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        self.language = language

    def set_textDirection(self,textDirection):
        """_summary_

        ltr		The direction that indicates the value of the resource is
                explicitly directionally isolated left-to-right text.
        rtl		The direction that indicates the value of the resource
                is explicitly directionally isolated right-to-left text.
        auto	The direction that indicates the value of the resource is
                explicitly directionally isolated text, and the direction is to
                be programmatically determined using the value.

        Args:
            textDirection (str): _description_
        """
        assert textDirection in ["ltr","rtl","auto"], "textDirection must be: ltr, rtl or auto"
        self.textDirection = textDirection

    def set_type(self,type):
        """Set type of the resource
        W3C:
        It is useful for clients to know the general type of a Web Resource in
        advance. If the client cannot render videos, then knowing that the Body
        is a video will allow it to avoid needlessly downloading a
        potentially large content stream. For resources that do not have
        obvious media types, such as many data formats, it is also useful
        for a client to know that a resource with the format text/csv should
        not simply be rendered as plain text, despite the first part of the
        media type, whereas application/pdf may be able to be rendered by the
        user agent despite the main type being 'application'.

        Args:
            type (str): The type of the resource.
        """
        assert type in TYPES, f"{type} is a non standard type add it to TYPES global variable"
        self.type = type

    def add_accessibility(self,accessibility):
        if unused(self.accessibility):
            self.accessibility = accessibility
        elif isinstance(self.accessibility,str):
            self.accessibility = [self.accessibility]
            self.accessibility.append(accessibility)

class _Purpose(object):
    def add_purpose(self,purpose):
        motivations = ["assessing",
                        "bookmarking",
                        "classifying",
                        "commenting",
                        "describing",
                        "editing",
                        "highlighting",
                        "identifying",
                        "linking",
                        "moderating",
                        "questioning",
                        "replying",
                        "tagging"]
        if purpose not in motivations:
            warnings.warn(f"Purpose not in {motivations}")
        setOrAppendStr(self,'purpose',purpose,str)

class TextualBody(_ImmutableType,_BodiesAndTargets,_Purpose):
    def __init__(self, target=Required()):
        super(TextualBody, self).__init__()
        self.id = None
        self.type = "TextualBody"
        self.value = Required("There must be exactly 1 value property associated with the TextualBody.")
        self.purpose = None


    def set_value(self,value):
        """The character sequence of the content of the Textual Body.

        Args:
            value (str): The character sequence of the content of the Textual Body.
        """
        self.value = value

class Choice(_CoreAttributes,_ImmutableType):
    def __init__(self):
        super(Choice, self).__init__()
        self.id = Recommended("The Choice may have exactly 1 IRI that identifies it.")
        self.items = Required()

    def add_resourceToItems(self,resource=None):
        """Add a resource to the items of the choice.

        Args:
            resource (_BodiesAndTargets, optional): The resource to be added.. Defaults to None.

        Returns:
            _BodiesAndTargets: If resource is None the resource.
        """ 
        return add_to(self, 'items', _BodiesAndTargets, resource, _BodiesAndTargets)

    def add_TextualBody_to_items(self,textualBody=None):
        """Add a TextualBody to the items list of the Choice element.

        Args:
            textualBody (TextualBody, optional): An instance of a TextualBody. Defaults to None.

        Returns:
            TextualBody: An instance of a TextualBody.
        """
        return addOrSet_to(self, 'items', TextualBody, textualBody, TextualBody)

    def add_SpecificResource_to_items(self,specificResource=None):
        return add_to(self, 'items', SpecificResource, specificResource, SpecificResource)

class Annotation(_CoreAttributes,_LifeCycleInformation,
                 _RightsInformationIdentities,_Source):
    """WADM resource
    """

    def __init__(self):
        super(Annotation, self).__init__()
        self.motivation = None
        self.body = Recommended("There should be 1 or more body relationships associated with an Annotation but there may be 0.")
        self.target = Required("There must be 1 or more target relationships associated with an Annotation.")
        self.bodyValue = None
        self.audience = None
        self.stylesheet = None

    def set_body(self,body=None):
        if body is None:
            self.body = _BodiesAndTargets()
            return self.body
        else:
            assert check_valid_URI(body), "Must be a valid URI"
            self.body = body

    def add_body(self,body=None):
        return add_to(self, 'body', _BodiesAndTargets, body, (_BodiesAndTargets, str))

    def add_target(self,target=None):
        return addOrSet_to(self, 'target', _BodiesAndTargets, target, (_BodiesAndTargets, str))

    def add_TextualBody(self,TextualBodyObj=None):
        return add_to(self,'body',TextualBody,TextualBodyObj,TextualBody)

    def add_SpecificResource_to_body(self,specificResource=None):
        return add_to(self,'body',SpecificResource,specificResource,SpecificResource)


    def add_ChoiceBody(self,ChoiceObj=None):
        """Add a Choice element to the body of the resource.

        Args:
            ChoiceObj (Choice, optional): An instance of a Choice. Defaults to 
            None.

        Returns:
            Choice: An instance of a Choice.
        """
        return addOrSet_to(self,"body",Choice,ChoiceObj,Choice)

    def set_target(self,target=None):
        if target is None:
            self.target = _BodiesAndTargets()
            return self.target
        else:
            assert check_valid_URI(target)
            self.target = target

    def set_audience(self,audience=None):
        if audience is None:
            self.audience = _IntendedAudience()
            return self.audience
        else:
            assert check_valid_URI(audience), "Must be a valid URI"
            self.audience = audience

    def add_audience(self,audience=None):
        return add_to(self, 'audience', _IntendedAudience, audience, (_IntendedAudience, str))

    def set_bodyValue(self,bodyValue):
        """Set the bodyValue of the annotation.
        must be a single xsd:string and the data type must not be expressed in
        the serialization.
        must not have a language associated with it.
        must be interpreted as if it were the value of the value property of a
        Textual Body.
        must be interpreted as if the Textual Body resource had a format
        property with the value text/plain.
        must not have the value of other properties of the Textual Body
        inferred from similar properties on the Annotation resource.

        Args:
            bodyValue (str): The bodyValue of the annotation.
        """
        assert isinstance(bodyValue,str), "Must be a single xsd:string"
        self.bodyValue = bodyValue

    def add_motivation(self, motivation):
        """set the motivation of the annotation.

        """

        motivations = ["assessing",
                        "bookmarking",
                        "classifying",
                        "commenting",
                        "describing",
                        "editing",
                        "highlighting",
                        "identifying",
                        "linking",
                        "moderating",
                        "questioning",
                        "replying",
                        "tagging"]
        if motivation not in motivations:
            warnings.warn("Motivation not in %s" % motivations)
        if unused(self.motivation):
            self.motivation = motivation
        elif isinstance(self.motivation,str):
            self.motivation = [self.motivation]
            self.motivation.append(motivation)

    def set_target_specific_resource(self, specificresource=None):
        """Set a specific resource as the target of the annotation.

        This function will set the target of the specific resource as an
        object.

        Examples:
            https://iiif.io/api/cookbook/recipe/0261-non-rectangular-commenting/
            >>> annotation.set_target_specific_resource()
            >>> annotation.target.set_source(canvas.id)
            >>> svg ="<svg xmlns='http://www.w3.org/2000/svg' ... > ... </svg>"
            >>> annotation.target.set_selector_as_SvgSelector(value=svg)

        Args:
            specificresource (`iiifpapi3.sepcificreosurce`, optional): a
                `iiifpapi3.sepcificreosurce` object. Defaults to None.

        Raises:
            ValueError: if you add the wrong object.

        Returns:
            `iiifpapi3.sepcificreosurce` : A reference to the object.
        """
        if specificresource is None:
            specificresource = SpecificResource()
            self.target = specificresource
            return specificresource
        else:
            if isinstance(specificresource, SpecificResource):
                self.target = specificresource
            else:
                raise ValueError(
                    "Trying to add wrong object to target in %s" %
                    self.__class__.__name__)

    def set_body_specific_resource(self, specificresource=None):
        """Set a specific resource as the target of the annotation.

        This function will set the target of the specific resource as an
        object.

        Examples:
            https://iiif.io/api/cookbook/recipe/0261-non-rectangular-commenting/
            >>> annotation.set_target_specific_resource()
            >>> annotation.target.set_source(canvas.id)
            >>> svg ="<svg xmlns='http://www.w3.org/2000/svg' ... > ... </svg>"
            >>> annotation.target.set_selector_as_SvgSelector(value=svg)

        Args:
            specificresource (`iiifpapi3.sepcificreosurce`, optional): a
                `iiifpapi3.sepcificreosurce` object. Defaults to None.

        Raises:
            ValueError: if you add the wrong object.

        Returns:
            `iiifpapi3.sepcificreosurce` : A reference to the object.
        """
        if specificresource is None:
            specificresource = SpecificResource()
            self.body = specificresource
            return specificresource
        else:
            if isinstance(specificresource, SpecificResource):
                self.body = specificresource
            else:
                raise ValueError(
                    "Trying to add wrong object to target in %s" %
                    self.__class__.__name__)
    
    def set_stylesheet(self,cssStylesheet=None):
        if cssStylesheet is None:
            self.stylesheet = CssStylesheet()
            return self.stylesheet
        elif isinstance(cssStylesheet,(str,CssStylesheet)):
            self.stylesheet = cssStylesheet

    def set_Independents_target(self,independentsTarget=None):
        if unused(self.target):
            if independentsTarget is None:
                self.target = Independents()
                return self.target
            else:
                assert isinstance(independentsTarget,Independents), "Must be Independets objects."
                self.target = independentsTarget

    def set_List_target(self,listTarget=None):
        if unused(self.target):
            if listTarget is None:
                self.target = List()
                return self.target
            else:
                assert isinstance(listTarget,List), "Must be Independets objects."
                self.target = listTarget

    def set_Composite_target(self,compositeTarget=None):
        if unused(self.target):
            if compositeTarget is None:
                self.target = Composite()
                return self.target
            else:
                assert isinstance(compositeTarget,Composite), "Must be Independets objects."
                self.target = compositeTarget

class _State(_ImmutableType):
    def __init__(self):
        self.type = self.__class__.__name__
        self.refinedBy = None

    def add_refinedBy(self,state):
        assert isinstance(state,(_State,_Selector)),"State must be a valid State"
        if self.refinedBy is None:
           self.refinedBy = state
        # if there is already a valid object we insert it on the list.
        elif isinstance(self.refinedBy,(_State,_Selector)):
            self.refinedBy = [self.refinedBy]
            self.refinedBy.append(state)
        # if there is already a list we just append
        elif isinstance(self.refinedBy,list):
            self.refinedBy.append(state)
        return state


class TimeState(_State):
    def __init__(self):
        super(TimeState, self).__init__()
        self.sourceDate = None
        self.sourceDateStart = None
        self.cached = None

    def add_sourceDate(self,sourceDate):
        """The timestamp at which the Source resource should be interpreted for
          the Annotation.

        There may be 0 or more sourceDate properties per TimeState.
        If there is more than 1, each gives an alternative timestamp at which
        the Source may be interpreted. The timestamp must be expressed in the
        xsd:dateTime format, and must use the UTC timezone expressed as "Z".
        If sourceDate is provided, then sourceDateStart and sourceDateEnd must
        not be provided.

        Args:
            sourceDate (date): the timestamp at which the Source resource should
            be interpreted for the Annotation.
        """
        setOrAppendStr(self,'sourceDate',sourceDate,str)

    def set_sourceDateStart(self,sourceDateStart):
        """	The timestamp that begins the interval over which the Source
        resource should be interpreted for the Annotation.

        There may be exactly 1 sourceDateStart property per TimeState.
        The timestamp must be expressed in the xsd:dateTime format, and must
        use the UTC timezone expressed as "Z". If sourceDateStart is provided
        then sourceDateEnd must also be provided.

        Args:
            sourceDateStart (_type_): _description_
        """
        self.sourceDateStart = sourceDateStart
        if self.sourceDateEnd is None:
            self.sourceDateEnd = Required("If sourceDateStart is provided then sourceDateEnd must also be provided.")

    def set_sourceDateEnd(self,sourceDateEnd):
        """The timestamp that ends the interval over which the Source resource 
        should be interpreted for the Annotation.

        There may be exactly 1 sourceDateEnd property per TimeState.
        The timestamp must be expressed in the xsd:dateTime format,
        and must use the UTC timezone expressed as "Z".
        If sourceDateEnd is provided then sourceDateStart must also be provided.

        Args:
            sourceDateEnd (str): The timestamp that ends the interval over
            which the Source resource should be interpreted for the Annotation.
        """
        self.sourceDateEnd = sourceDateEnd
        if self.set_sourceDateStart is None:
            self.sourceDateStart = Required("If sourceDateEnd is provided then sourceDateStart must also be provided.")

    def add_cached(self,cached):
        """A link to a copy of the Source resource's representation,
        appropriate for the Annotation.

        There may be 0 or more cached relationships per TimeState. If there is
        more than 1, each gives an alternative copy of the representation.


        Args:
            cached (str): A link to a copy of the Source resource's
            representation, appropriate for the Annotation.
        """
        setOrAppendStr(self,"cached",cached,str)

class HttpRequestState(_State):
    def __init__(self):
        super(HttpRequestState, self).__init__()
        self.value = None

    def set_value(self,value):
        """The HTTP request headers to send as a single, complete string.

        An HttpRequestState must have exactly 1 value property.

        Args:
            value (str): The HTTP request headers to send as a single, complete
            string.
        """
        self.value = value

class CssStylesheet(object):
    def __init__(self):
        super(CssStylesheet, self).__init__()
        self.type = None

    def set_type(self):
        """Set the type of CssStylesheet.
        Note: CSS Stylesheets may have a type and if included the value must be
        CssStylesheet.
        """
        self.type = "CssStylesheet"
    
    def set_value(self,value):
        #TODO: set_value is not defined in the spec.
        self.value = value

class SpecificResource(_CoreAttributes,_Purpose,_Source,_SetSelector):
    """WADM Web Annotation Data Model resource

    """
    def __init__(self):
        super(SpecificResource, self).__init__()
        self.id = Recommended("An ID is recommended.")
        self.source = None
        self.purpose = None
        self.scope = None
        self.state = None
        self.styleClass = None
        self.renderedVia = None

    def set_selector_as_PointSelector(self):
        """Set the selectof of the SpecificReource as a PointSelector.

        Returns:
            iiifpapi3.PointSelector: A reference to an empty
                iiifpapi3.PointSelector
        """
        ps = PointSelector()
        self.selector = ps
        return ps

    def set_selector_as_SvgSelector(self, value=None):
        """Set the selector to an SvgSelector or to a SVG string.

        Args:
            value (str, optional): An SVG as a string. Defaults to None.

        Returns:
            iiifpapi3.SvgSelector: An instance of iiifpapi3.SvgSelector
        """
        ss = SvgSelector()
        if value is not None:
            ss.set_value(value)
        self.selector = ss
        return ss

    def set_selector_as_FragmentSelector(self):
        self.selector = FragmentSelector()
        return self.selector
    
    def set_selector_as_CssSelector(self):
        self.selector = CssSelector()
        return self.selector
    
    def set_selector_as_XPathSelector(self):
        self.selector = XPathSelector()
        return self.selector
    
    def set_selector_as_TextPositionSelector(self):
        self.selector = TextPositionSelector()
        return self.selector
    
    def set_selector_as_DataPositionSelector(self):
        self.selector = DataPositionSelector()
        return self.selector
    
    def set_selector_as_TextQuoteSelector(self):
        """Set the selector to an TextQuoteSelector or to a SVG string.

        Args:
            value (str, optional): An SVG as a string. Defaults to None.

        Returns:
            iiifpapi3.SvgSelector: An instance of iiifpapi3.SvgSelector
        """
        ss = TextQuoteSelector()
        self.selector = ss
        return ss
    
    def set_selector_as_RangeSelector(self):
        self.selector = RangeSelector()
        return self.selector

    def set_state(self,state):
        # TODO: specification is not clear how state object is defined.
        self.state = state

    def add_TimeState(self,timeState=None):
        """_summary_

        Args:
            timeState (_type_, optional): _description_. Defaults to None.

        Returns:
            TimeState: A TimeState object.
        """
        return addOrSet_to(self,"state",TimeState,timeState,_State)
    
    def add_HttpRequestState(self,httpRequestState=None):
        return addOrSet_to(self,"state",HttpRequestState,httpRequestState,_State)
    
    def set_styleClass(self,styleClass):
        self.styleClass = styleClass

    def add_renderedVia(self,renderedVia=None):
        return addOrSet_to(self,"renderedVia",Software,renderedVia,Software)
    
    def add_scope(self,scope):
        """The relationship between a Specific Resource and the resource that provides the scope or context for it in
        this Annotation.

        Args:
            scope (str): The relationship between a Specific Resource and the resource that provides the scope or
            context for it in this Annotation.
        """
        addOrSet_to(self,"scope",str,scope,str)


class AnnotationPage(_CoreAttributes,_LifeCycleInformation):
    """WADM resource.
    """
    # TODO: AnnotationPage type MUST be AnnotationPage?
    def __init__(self):
        super(AnnotationPage, self).__init__()
        self.items = Recommended(
            "The annotation page should incude at least one item.")

    def add_item(self, item):
        """Add an item (Annotation) to the AnnotationPage.

        Same as `add_annotation_to_items` but doesn't return.

        An Annotation Page should have the items property with at least one
        item. Each item must be an Annotation.

        Args:
            item (Annotation): The Annotation
        """
        add_to(self, 'items', Annotation, item)

    def add_annotation_to_items(self, annotation=None, target=None):
        return add_to(self, 'items', Annotation, annotation, target=target)

    def set_partOf(self,partOf=None):
        """The relationship between the Page and the Annotation Collection that
        it is part of.

        Each Page should have a exactly 1 partOf relationship, with the value
        being either the IRI of the Collection or an object with some or all of the Collections properties, including at least its id.


        Args:
            partOf (URI,AnnotationCollection): _description_
        """
        if partOf is None:
            self.partOf = AnnotationCollection()
            return self.partOf
        assert check_valid_URI(partOf) or isinstance(partOf,AnnotationCollection), "Should be string or URI"
        self.partOf = partOf

    def add_annotation_to_items(self,annotation=None):
        """The list of Annotations that are the members of the Page.
        Each Page must have an array of 1 or more Annotations as the value of
        items.

        Args:
            annotation (Annotation, optional): An Annotation to be inserted.

        Returns:
            Annotation: An Annotation is annotation is set to None
        """
        return add_to(self,"items",Annotation,annotation,Annotation)

    def set_next(self,next):
        """A reference to the next Page in the sequence of pages that make up
        the Collection.

        If the current page is not the last page in the Collection, it must
        have a reference to the IRI of the page that follows it.

        Args:
            next (str): A reference to the next Page in the sequence of pages
            that make up the Collection.
        """
        assert check_valid_URI(next), "Next should be a valid URI"
        self.next = next

    def set_prev(self,prev):
        """A reference to the previous Page in the sequence of pages that make
        up the Collection.

        If the current page is not the first page in the Collection, it should
        have a reference to the IRI of the page that it follows.

        Args:
            prev (str): A reference to the previous Page in the sequence of 
            pages that make up the Collection.
        """
        self.prev = prev

    def set_startIndex(self,startIndex):
        """The relative position of the first Annotation in the items list,
        relative to the Annotation Collection. The first entry in the first
        page is considered to be entry 0.

        Each Page should have exactly 1 startIndex, and must not have more than
        1. The value must be an xsd:nonNegativeInteger.

        Args:
            startIndex (str): The relative position of the first Annotation in
            the items list, relative to the Annotation Collection.
        """
        self.startIndex = startIndex

class AnnotationCollection(_CoreAttributes,_LifeCycleInformation):
    """WADM resource.

    https://iiif.io/api/presentation/3.0/#58-annotation-collection

    Annotation Collections represent groupings of Annotation Pages that should
    be managed as a single whole, regardless of which Canvas or resource they
    target. This allows, for example, all of the Annotations that make up a
    particular translation of the text of a book to be collected together. A
    client might then present a user interface that allows all of the
    Annotations in an Annotation Collection to be displayed or hidden according
    to the user’s preference.

    """
    def __init__(self):
        super(AnnotationCollection, self).__init__()
        self.label = Recommended("An Annotation Collection should have the"
                                 "label property with at least one entry.")
        self.first = None
        self.last = None

    def set_id(self, objid, extendbase_url=None):
        """Set the ID of the object

        https://iiif.io/api/presentation/3.0/#id
        https://iiif.io/api/presentation/3.0/#58-annotation-collection

        WADM: Annotation Collections must have a URI, and it should be an
        HTTP(S) URI.

        Note:
            Usually ID must be HTTP(S) in this case it seems not.

        Args:
            objid (str, optional): A string corresponding to the ID of the
                object `id = objid`.Defaults to None.
            extendbase_url (str , optional): A string containing the URL part
                to be joined with the iiifpapi3.BASE_URL:
                `id = iiifpapi3.BASE_URL + extendbase_url`. Defaults to None.
        """
        try:
            return super().set_id(objid=objid, extendbase_url=extendbase_url)
        except AssertionError:
            warnings.warn("%s is not an http, AnnotationCollections should use HTTP(S) URI")
            self.id = objid

    def set_total(self,total):
        """The total number of Annotations in the Collection.

        Collections should have exactly 1 total, and if present it must be an 
        xsd:nonNegativeInteger.

        Args:
            total (int): The total number of Annotations in the Collection.
        """
        self.total = total

    def set_first(self,first=None):
        """The first page of Annotations that are included within the
        Collection.

        A Collection that has a total number of Annotations greater than 0 must
        have exactly 1 first page of Annotations. The first Page may be
        embedded within the representation of the Collection, or it may be
        given as an IRI.

        Args:
            first (str): The first page of Annotations that are included within
            the Collection. Default None.
        """
        assert isinstance(first,(AnnotationPage,str,type(None))),"Frist must be str or AnnotationPage"
        if first is None:
            self.first = AnnotationPage()
        else:
            self.first = first
        return self.first
    
    def set_last(self,last=None):
        """The last page of Annotations that are included within the Collection.

        A Collection that has a total number of Annotations greater than 0
        should have a reference to the IRI of the last page of Annotations.

        Args:
            last (strt): The last page of Annotations that are included within
            the Collection.
        """
        assert isinstance(last,(AnnotationPage,str,type(None))),"Frist must be str or AnnotationPage"
        if last is None:
            self.last = AnnotationPage()
        else:
            self.last = last
        return self.last

    def add_label(self,label):
        addOrSet_to(self,"label",str,label,str)


class _SetsOfBodiesAndTargets(_CoreAttributes):
    def __init__(self):
        super(_SetsOfBodiesAndTargets, self).__init__()
        self.items = []
        self.id = None

    def add_target(self,target=None):
        return add_to(self, 'items', _BodiesAndTargets, target, (_BodiesAndTargets, str))

    def add_SpecificResource_target(self,SpecificResource=None):
        return add_to(self, 'items', SpecificResource, target, (SpecificResource, str))

class List(_SetsOfBodiesAndTargets):
    def __init__(self):
        super(List, self).__init__()

class Composite(_SetsOfBodiesAndTargets):
    def __init__(self):
        super(Composite, self).__init__()

class Independents(_SetsOfBodiesAndTargets):
    def __init__(self):
        super(Independents, self).__init__()