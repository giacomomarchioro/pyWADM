# EXAMPLE 32: HTTP Request State
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno32",
  "type": "Annotation",
  "body": "http://example.org/description1",
  "target": {
    "source": "http://example.org/resource1",
    "state": {
      "type": "HttpRequestState",
      "value": "Accept: application/pdf"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno32")
anno.set_body("http://example.org/description1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/resource1")
ts = anno.target.add_HttpRequestState()
ts.set_value("Accept: application/pdf")
anno.to_json()