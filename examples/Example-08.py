r= {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno8",
  "type": "Annotation",
  "target": "http://example.org/ebook1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno8")
anno.target = "http://example.org/ebook1"
anno.to_json()