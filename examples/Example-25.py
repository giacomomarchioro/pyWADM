# EXAMPLE 25: Data Position Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno25",
  "type": "Annotation",
  "body": "http://example.org/note1",
  "target": {
    "source": "http://example.org/diskimg1",
    "selector": {
      "type": "DataPositionSelector",
      "start": 4096,
      "end": 4104
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno25")
anno.set_body("http://example.org/note1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/diskimg1")
anno.target.set_selector_as_DataPositionSelector()
anno.target.selector.set_start(4096)
anno.target.selector.set_end(4104)
anno.to_json()