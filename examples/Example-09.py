r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno9",
  "type": "Annotation",
  "body": [
    "http://example.org/description1",
    {
      "type": "TextualBody",
      "value": "tag1"
    }
  ],
  "target": [
    "http://example.org/image1",
    "http://example.org/image2"
  ]
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno9")
anno.add_body("http://example.org/description1")
tb = anno.add_TextualBody()
tb.set_value("tag1")
anno.add_target("http://example.org/image1")
anno.add_target("http://example.org/image2")
anno.to_json()