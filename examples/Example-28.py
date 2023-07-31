# EXAMPLE 28: Range Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno28",
  "type": "Annotation",
  "body": "http://example.org/comment1",
  "target": {
    "source": "http://example.org/page1.html",
    "selector": {
      "type": "RangeSelector",
      "startSelector": {
        "type": "XPathSelector",
        "value": "//table[1]/tr[1]/td[2]"
      },
      "endSelector": {
        "type": "XPathSelector",
        "value": "//table[1]/tr[1]/td[4]"
      }
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno28")
anno.set_body("http://example.org/comment1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/page1.html")
anno.target.set_selector_as_RangeSelector()
startSelector = WADM.XPathSelector()
startSelector.set_value("//table[1]/tr[1]/td[2]")
endSelector = WADM.XPathSelector()
endSelector.set_value("//table[1]/tr[1]/td[4]")
anno.target.selector.set_endSelector(endSelector)
anno.target.selector.set_startSelector(startSelector)
anno.to_json()