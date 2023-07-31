# EXAMPLE 35: CSS Style, embedded
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno35",
  "type": "Annotation",
  "stylesheet": {
    "type": "CssStylesheet",
    "value": ".red { color: red }"
  },
  "body": "http://example.org/body1",
  "target": {
    "source": "http://example.org/target1",
    "styleClass": "red"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno35")
anno.set_stylesheet()
anno.stylesheet.set_value(".red { color: red }")
anno.stylesheet.set_type()
anno.set_body("http://example.org/body1")
# We force the type to None
anno.set_target_specific_resource()
anno.target.type = None
anno.target.set_source("http://example.org/target1")
anno.target.set_styleClass("red")
anno.to_json()