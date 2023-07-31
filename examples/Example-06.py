r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno6",
  "type": "Annotation",
  "bodyValue": "Comment text",
  "target": "http://example.org/target1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno6")
anno.set_bodyValue("Comment text")
anno.target = "http://example.org/target1"
anno.to_json()