# EXAMPLE 26: SVG Selector
# EXAMPLE 30: State
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno30",
  "type": "Annotation",
  "body": "http://example.org/note1",
  "target": {
    "source": "http://example.org/page1",
    "state": {
      "id": "http://example.org/state1"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno30")
anno.set_body("http://example.org/note1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/page1")
# TODO: Never defined in specs!
state = {"id":"http://example.org/state1"}
anno.target.set_state(state)
anno.to_json()