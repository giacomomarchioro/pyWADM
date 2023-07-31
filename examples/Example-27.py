# EXAMPLE 27: SVG Selector, embedded
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno27",
  "type": "Annotation",
  "body": "http://example.org/road1",
  "target": {
    "source": "http://example.org/map1",
    "selector": {
      "type": "SvgSelector",
      "value": "<svg:svg> ... </svg:svg>"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno27")
anno.set_body("http://example.org/road1")
anno.set_target_specific_resource()
# We force the type to None
anno.target.type = None
anno.target.set_source("http://example.org/map1")
anno.target.set_selector_as_SvgSelector()
anno.target.selector.set_value("<svg:svg> ... </svg:svg>")
anno.to_json()