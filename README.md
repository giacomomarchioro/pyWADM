# pyWDAM

----------------
This is a Python module built for easing the construction of JSON object compliant with the [Web Annotation Data Model](https://www.w3.org/TR/annotation-model/) in a production environment.

## Installation
The library uses only standard libraries and can be installed using `pip`.

Development :

    pip install git+https://github.com/giacomomarchioro/pyWADM

## Basic usage
The module maps the API structure to Python classes. The user `set_` objects that can have only one value (e.g. `id`) and `add_` objects that can have multiple entities (e.g. `labels`).

The easiest way to get started is to have a look at the examples in the [Recommendation](https://www.w3.org/TR/annotation-model/) and modify the example in the `examples`` folder in this repository. For instance:

```python
# EXAMPLE 1: Basic Annotation Model
from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno1")
anno.set_body("http://example.org/post1")
anno.set_target("http://example.com/page1")
anno.to_json()
```
If `set_` or `add_` require a specific Class they can be left with no arguments, they will return an instance of the class needed to be populated.
```python
# EXAMPLE 40: Annotation Collection with Embedded Page
from wadm import WADM
anno = WADM.AnnotationCollection()
anno.set_id("http://example.org/collection1")
anno.add_label("Two Annotations")
anno.set_total(2)
annop = anno.set_first()
annop.set_id("http://example.org/page1")
annop.set_startIndex(0)
a1 = annop.add_annotation_to_items()
a1.set_id("http://example.org/anno1")
a1.set_body("http://example.net/comment1")
a1.set_target("http://example.com/book/chapter1")
a2 = annop.add_annotation_to_items()
a2.set_target("http://example.com/book/chapter2")
a2.set_body("http://example.net/comment2")
a2.set_id("http://example.org/anno2")
anno.to_json()
```

## Debug the object
When you are populating a new WADM object from scratch some helpful functions can be
used for spotting errors.

`.inspect()` method returns a JSON representation of the object where the
recommended and required fields are shown:

```python
from wadm import WADM
anno = WADM.Annotation()
anno.inspect()
```

`.show_errors_in_browser()` method open a new browser tab highlighting the 
required and recommended fields.

```python
anno.show_errors_in_browser()
```

## Acknowledgements
The package is provided by the [Laboratorio di Studi Medievali e Danteschi](https://sites.hss.univr.it/laboratori_integrati/laboratorio-lamedan/) of the [University of Verona](https://www.univr.it/en/home)

<img src="https://i.ibb.co/tcTNXRP/layerlores.png" alt="LaMeDan Logo" width="250">

