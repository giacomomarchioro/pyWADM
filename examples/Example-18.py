# EXAMPLE 18: Resource with Purpose
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno18",
  "type": "Annotation",
  "body": {
    "type": "SpecificResource",
    "purpose": "tagging",
    "source": "http://example.org/city1"
  },
  "target": {
    "id": "http://example.org/photo1",
    "type": "Image"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno18")
anno.set_body_specific_resource()
anno.body.add_purpose("tagging")
anno.body.set_source("http://example.org/city1")
anno.set_target()
anno.target.set_type("Image")
anno.target.set_id("http://example.org/photo1")
anno.to_json()