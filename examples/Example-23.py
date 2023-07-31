# EXAMPLE 23: Text Quote Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno23",
  "type": "Annotation",
  "body": "http://example.org/comment1",
  "target": {
    "source": "http://example.org/page1",
    "selector": {
      "type": "TextQuoteSelector",
      "exact": "anotation",
      "prefix": "this is an ",
      "suffix": " that has some"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno23")
anno.set_body("http://example.org/comment1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/page1")
anno.target.set_selector_as_TextQuoteSelector()
anno.target.selector.set_exact("anotation")
anno.target.selector.set_prefix("this is an ")
anno.target.selector.set_suffix(" that has some")
anno.to_json()