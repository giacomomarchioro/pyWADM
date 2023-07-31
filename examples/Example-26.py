# EXAMPLE 26: SVG Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno26",
  "type": "Annotation",
  "body": "http://example.org/road1",
  "target": {
    "source": "http://example.org/map1",
    "selector": {
      "id": "http://example.org/svg1",
      "type": "SvgSelector"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno26")
anno.set_body("http://example.org/road1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/map1")
anno.target.set_selector_as_SvgSelector()
# TODO: NOT IN SPECS!
anno.target.selector.id = "http://example.org/svg1"
anno.to_json()