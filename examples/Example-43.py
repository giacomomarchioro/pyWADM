# EXAMPLE 43: List
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno40",
  "type": "Annotation",
  "motivation": "tagging",
  "body": {
    "type": "TextualBody",
    "value": "important"
  },
  "target": {
    "type": "List",
    "items": [
      "http://example.com/book/page1",
      "http://example.com/book/page2",
      "http://example.com/book/page3",
      "http://example.com/book/page4"
    ]
  }
}
from wadm import WADM

anno = WADM.Annotation()
anno.set_id("http://example.org/anno40")
anno.add_motivation("tagging")
tb = anno.add_TextualBody()
tb.set_value("Important")
anno.set_List_target()
anno.target.add_target("http://example.com/page1")
anno.target.add_target("http://example.org/page6")
anno.target.add_target("http://example.net/page5")
anno.to_json()