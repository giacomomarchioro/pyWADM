r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno17",
  "type": "Annotation",
  "canonical": "urn:uuid:dbfb1861-0ecf-41ad-be94-a584e5c4f1df",
  "via": "http://other.example.org/anno1",
  "body": {
    "id": "http://example.net/review1",
    "rights": "http://creativecommons.org/licenses/by/4.0/"
  },
  "target": "http://example.com/product1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno17")
anno.set_canonical("urn:uuid:dbfb1861-0ecf-41ad-be94-a584e5c4f1df")
anno.add_via("http://other.example.org/anno1")
anno.set_body()
anno.body.set_id("http://example.net/review1")
anno.body.add_rights("http://creativecommons.org/licenses/by/4.0/")
anno.set_target("http://example.com/product1")
anno.to_json()