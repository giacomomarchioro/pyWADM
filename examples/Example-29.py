# EXAMPLE 29: Refinement of Selection
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno29",
  "type": "Annotation",
  "body": "http://example.org/comment1",
  "target": {
    "source": "http://example.org/page1",
    "selector": {
      "type": "FragmentSelector",
      "value": "para5",
      "refinedBy": {
        "type": "TextQuoteSelector",
        "exact": "Selected Text",
        "prefix": "text before the ",
        "suffix": " and text after it"
      }
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno29")
anno.set_body("http://example.org/comment1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/page1")
anno.target.set_selector_as_FragmentSelector()
anno.target.selector.set_value("para5")
tq = WADM.TextQuoteSelector()
tq.set_exact("Selected Text")
tq.set_prefix("text before the ")
tq.set_suffix(" and text after it")
anno.target.selector.add_refinedBy(tq)
anno.to_json()