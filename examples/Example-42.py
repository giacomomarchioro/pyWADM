# EXAMPLE 42: Composite
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno42",
  "type": "Annotation",
  "motivation": "commenting",
  "body": {
    "type": "TextualBody",
    "value": "These pages together provide evidence of the conspiracy"
  },
  "target": {
    "type": "Composite",
    "items": [
      "http://example.com/page1",
      "http://example.org/page6",
      "http://example.net/page4"
    ]
  }
}
from wadm import WADM

anno = WADM.Annotation()
anno.set_id("http://example.org/anno39")
anno.add_motivation("commenting")
tb = anno.add_TextualBody()
tb.set_value("These pages together provide evidence of the conspiracy")
anno.set_Composite_target()
anno.target.add_target("http://example.com/page1")
anno.target.add_target("http://example.org/page6")
anno.target.add_target("http://example.net/page5")
anno.to_json()