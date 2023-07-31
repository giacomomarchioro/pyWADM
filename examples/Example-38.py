# EXAMPLE 38: Annotation Collection
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/collection1",
  "type": "AnnotationCollection",
  "label": "Steampunk Annotations",
  "creator": "http://example.com/publisher",
  "total": 42023,
  "first": "http://example.org/page1",
  "last": "http://example.org/page42"
}

from wadm import WADM
anno = WADM.AnnotationCollection()
anno.set_id("http://example.org/collection1")
anno.add_label("Steampunk Annotations")
anno.set_creator("http://example.com/publisher")
anno.set_total(42023)
anno.set_first("http://example.org/page1")
anno.set_last("http://example.org/page42")
anno.to_json()