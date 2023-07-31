# EXAMPLE 39: Annotation Page
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/page1",
  "type": "AnnotationPage",
  "partOf": {
    "id": "http://example.org/collection1",
    "label": "Steampunk Annotations",
    "total": 42023
  },
  "next": "http://example.org/page2",
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

from wadm import WADM

anno = WADM.AnnotationPage()
anno.set_id("http://example.org/page1")
po = anno.set_partOf()
po.set_id("http://example.org/collection1")
po.type = None
po.add_label("Steampunk Annotations")
po.set_total(42023)
anno.set_next("http://example.org/page2")
anno.set_startIndex(0)
a1 =  anno.add_annotation_to_items()
a1.set_id("http://example.org/anno1")
a1.set_body("http://example.net/comment1")
a1.set_target("http://example.com/book/chapter1")
a2 =  anno.add_annotation_to_items()
a2.set_id("http://example.org/anno2")
a2.set_body("http://example.net/comment2")
a2.set_target("http://example.com/book/chapter2")
anno.to_json()