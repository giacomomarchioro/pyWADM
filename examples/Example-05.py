r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno5",
  "type": "Annotation",
  "body": {
    "type" : "TextualBody",
    "value" : "<p>j'adore !</p>",
    "format" : "text/html",
    "language" : "fr"
  },
  "target": "http://example.org/photo1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno5")
anno.body = WADM.TextualBody()
anno.body.value = "<p>j'adore !</p>"
anno.body.format = "text/html"
anno.body.language = "fr"
anno.target = "http://example.org/photo1"
anno.to_json()