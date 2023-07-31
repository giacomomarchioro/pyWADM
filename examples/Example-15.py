r= {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno15",
  "type": "Annotation",
  "motivation": "bookmarking",
  "body": [
    {
      "type": "TextualBody",
      "value": "readme",
      "purpose": "tagging"
    },
    {
      "type": "TextualBody",
      "value": "A good description of the topic that bears further investigation",
      "purpose": "describing"
    }
  ],
  "target": "http://example.com/page1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno15")
anno.add_motivation("bookmarking")
b1 = anno.add_TextualBody()
b1.set_value("readme")
b1.add_purpose("tagging")
b2 = anno.add_TextualBody()
b2.set_value("A good description of the topic that bears further investigation")
b2.add_purpose("describing")
anno.set_target("http://example.com/page1")
anno.to_json()
