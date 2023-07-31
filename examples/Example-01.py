r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno1",
  "type": "Annotation",
  "body": "http://example.org/post1",
  "target": "http://example.com/page1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno1")
anno.set_body("http://example.org/post1")
anno.set_target("http://example.com/page1")
anno.to_json()