# EXAMPLE 24: Text Position Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno24",
  "type": "Annotation",
  "body": "http://example.org/review1",
  "target": {
    "source": "http://example.org/ebook1",
    "selector": {
      "type": "TextPositionSelector",
      "start": 412,
      "end": 795
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno24")
anno.set_body("http://example.org/review1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/ebook1")
anno.target.set_selector_as_TextPositionSelector()
anno.target.selector.set_start(412)
anno.target.selector.set_end(795)
anno.to_json()