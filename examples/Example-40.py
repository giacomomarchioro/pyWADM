# EXAMPLE 40: Annotation Collection with Embedded Page
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/collection1",
  "type": "AnnotationCollection",
  "label": "Two Annotations",
  "total": 2,
  "first": {
    "id": "http://example.org/page1",
    "type": "AnnotationPage",
    "startIndex": 0,
    "items": [
      {
        "id": "http://example.org/anno1",
        "type": "Annotation",
        "body": "http://example.net/comment1",
        "target": "http://example.com/book/chapter1"
      },
      {
        "id": "http://example.org/anno2",
        "type": "Annotation",
        "body": "http://example.net/comment2",
        "target": "http://example.com/book/chapter2"
      }
    ]
  }
}
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