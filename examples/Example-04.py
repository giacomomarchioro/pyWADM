r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno4",
  "type": "Annotation",
  "body": "http://example.org/description1",
  "target": {
    "id": "http://example.com/image1#xywh=100,100,300,300",
    "type": "Image",
    "format": "image/jpeg"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno4")
anno.set_body("http://example.org/description1")
anno.set_target()
anno.target.set_id("http://example.com/image1#xywh=100,100,300,300")
anno.target.set_type("Image")
anno.target.set_format("image/jpeg")
anno.to_json()