# EXAMPLE 20: Fragment Selector
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno20",
  "type": "Annotation",
  "body": {
    "source": "http://example.org/video1",
    "purpose": "describing",
    "selector": {
      "type": "FragmentSelector",
      "conformsTo": "http://www.w3.org/TR/media-frags/",
      "value": "t=30,60"
    }
  },
  "target": "http://example.org/image1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno20")
anno.set_body_specific_resource()
# delete type
anno.body.type = None
anno.body.set_source("http://example.org/video1")
anno.body.add_purpose("describing")
anno.body.set_selector_as_FragmentSelector()
anno.body.selector.set_conformsTo("http://www.w3.org/TR/media-frags/")
anno.body.selector.set_value("t=30,60")
anno.set_target("http://example.org/image1")
anno.to_json()