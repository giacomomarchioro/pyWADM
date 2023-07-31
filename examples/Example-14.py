r= {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno14",
  "type": "Annotation",
  "motivation": "commenting",
  "body": "http://example.net/comment1",
  "target": {
    "id": "http://example.com/video1",
    "type": "Video",
    "accessibility": "captions"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno14")
anno.set_body("http://example.net/comment1")
anno.add_motivation("commenting")
anno.set_target()
anno.target.set_id("http://example.com/video1")
anno.target.set_type("Video")
anno.target.add_accessibility("captions")
anno.to_json()