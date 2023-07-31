# EXAMPLE 33: Refinement of States
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno33",
  "type": "Annotation",
  "body": "http://example.org/comment1",
  "target": {
    "source": "http://example.org/ebook1",
    "state": {
      "type": "TimeState",
      "sourceDate": "2016-02-01T12:05:23Z",
      "refinedBy": {
        "type": "HttpRequestState",
        "value": "Accept: application/pdf",
        "refinedBy": {
          "type": "FragmentSelector",
          "value": "page=10",
          "conformsTo": "http://tools.ietf.org/rfc/rfc3778"
        }
      }
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno33")
anno.set_body("http://example.org/comment1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/ebook1")
ts = anno.target.add_TimeState()
ts.add_sourceDate("2016-02-01T12:05:23Z")
rs = WADM.HttpRequestState()
rs.set_value("Accept: application/pdf")
ts.add_refinedBy(rs)
fs = WADM.FragmentSelector()
fs.set_value("page=10")
fs.set_conformsTo("http://tools.ietf.org/rfc/rfc3778")
rs.add_refinedBy(fs)
anno.to_json()