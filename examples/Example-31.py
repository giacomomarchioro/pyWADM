# EXAMPLE 31: Time State
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno31",
  "type": "Annotation",
  "body": "http://example.org/note1",
  "target": {
    "source": "http://example.org/page1",
    "state": {
      "type": "TimeState",
      "cached": "http://archive.example.org/copy1",
      "sourceDate": "2015-07-20T13:30:00Z"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno31")
anno.set_body("http://example.org/note1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/page1")
# TODO: Never defined in specs!
ts = anno.target.add_TimeState()
ts.add_cached("http://archive.example.org/copy1")
ts.add_sourceDate("2015-07-20T13:30:00Z")
anno.to_json()