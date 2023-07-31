# EXAMPLE 37: Scope
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno37",
  "type": "Annotation",
  "body": "http://example.org/note1",
  "target": {
    "source": "http://example.org/image1",
    "scope": "http://example.org/page1"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno37")
anno.set_body("http://example.org/note1")
# We force the type to None
anno.set_target_specific_resource()
anno.target.type = None
anno.target.set_source("http://example.org/image1")
anno.target.add_scope("http://example.org/page1")
anno.to_json()