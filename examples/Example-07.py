r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno7",
  "type": "Annotation",
  "body": {
    "type": "TextualBody",
    "value": "Comment text",
    "format": "text/plain"
  },
  "target": "http://example.org/target1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno7")
anno.body = WADM.TextualBody()
anno.body.value = "Comment text"
anno.body.format = "text/plain"
anno.target = "http://example.org/target1"
anno.to_json()