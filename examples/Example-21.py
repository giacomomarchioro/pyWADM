# EXAMPLE 21: CSS Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno21",
  "type": "Annotation",
  "body": "http://example.org/note1",
  "target": {
    "source": "http://example.org/page1.html",
    "selector": {
      "type": "CssSelector",
      "value": "#elemid > .elemclass + p"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno21")
anno.set_body("http://example.org/note1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/page1.html")
anno.target.set_selector_as_CssSelector()
anno.target.selector.set_value("#elemid > .elemclass + p")
anno.to_json()