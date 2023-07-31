# EXAMPLE 34: CSS Style
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno34",
  "type": "Annotation",
  "stylesheet": "http://example.org/style1",
  "body": "http://example.org/comment1",
  "target": {
    "source": "http://example.org/document1",
    "styleClass": "red"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno34")
anno.set_stylesheet("http://example.org/style1")
anno.set_body("http://example.org/comment1")
# We force the type to None
anno.set_target_specific_resource()
anno.target.type = None
anno.target.set_source("http://example.org/document1")
anno.target.set_styleClass("red")
anno.to_json()