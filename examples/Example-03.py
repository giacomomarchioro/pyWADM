r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno3",
  "type": "Annotation",
  "body": {
    "id": "http://example.org/video1",
    "type": "Video"
  },
  "target": {
    "id": "http://example.org/website1",
    "type": "Text"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno3")
anno.set_body()
anno.body.set_id("http://example.org/video1")
anno.body.set_type("Video")
anno.set_target()
anno.target.set_id("http://example.org/website1")
anno.target.set_type("Text")
anno.to_json()