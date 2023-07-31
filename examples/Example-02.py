r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno2",
  "type": "Annotation",
  "body": {
    "id": "http://example.org/analysis1.mp3",
    "format": "audio/mpeg",
    "language": "fr"
  },
  "target": {
    "id": "http://example.gov/patent1.pdf",
    "format": "application/pdf",
    "language": ["en", "ar"],
    "textDirection": "ltr",
    "processingLanguage": "en"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno2")
anno.set_body()
anno.body.set_id("http://example.org/analysis1.mp3")
anno.body.set_format("audio/mpeg")
anno.body.set_language("fr")
anno.set_target()
anno.target.set_id("http://example.gov/patent1.pdf")
anno.target.set_format("application/pdf")
anno.target.add_language("en")
anno.target.add_language("ar")
anno.target.set_textDirection("ltr")
anno.target.set_processingLanguage("en")
anno.to_json()