r= {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno13",
  "type": "Annotation",
  "audience": {
    "id": "http://example.edu/roles/teacher",
    "type": "schema:EducationalAudience",
    "schema:educationalRole": "teacher"
  },
  "body": "http://example.net/classnotes1",
  "target": "http://example.com/textbook1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno13")
anno.set_audience()
anno.audience.set_id("http://example.edu/roles/teacher")
anno.audience.set_type("schema:EducationalAudience")
anno.audience.add_schemaProperty("schema:educationalRole","teacher")
anno.set_body("http://example.net/classnotes1")
anno.set_target("http://example.com/textbook1")
anno.to_json()

import dictdiffer

for i in dictdiffer.diff(r,anno.to_json()):
    print(i)