r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno10",
  "type": "Annotation",
  "body": {
    "type": "Choice",
    "items": [
      {
        "id": "http://example.org/note1",
        "language": "en"
      },
      {
        "id": "http://example.org/note2",
        "language": "fr"
      }
    ]
  },
  "target": "http://example.org/website1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno10")
choice = anno.add_ChoiceBody()
r1 = choice.add_resourceToItems()
r1.set_language("en")
r1.set_id("http://example.org/note1")
r2 = choice.add_resourceToItems()
r2.set_language("fr")
r2.set_id("http://example.org/note2")
anno.set_target("http://example.org/website1")
anno.to_json()