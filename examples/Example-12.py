r= {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno12",
  "type": "Annotation",
  "creator": {
    "id": "http://example.org/user1",
    "type": "Person",
    "name": "My Pseudonym",
    "nickname": "pseudo",
    "email_sha1": "58bad08927902ff9307b621c54716dcc5083e339"
  },
  "generator": {
    "id": "http://example.org/client1",
    "type": "Software",
    "name": "Code v2.1",
    "homepage": "http://example.org/client1/homepage1"
  },
  "body": "http://example.net/review1",
  "target": "http://example.com/restaurant1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno12")
anno.set_creator()
anno.creator.set_id("http://example.org/user1")
anno.creator.set_type("Person")
anno.creator.set_name("My Pseudonym")
anno.creator.set_nickname("pseudo")
anno.creator.set_email_sha1("58bad08927902ff9307b621c54716dcc5083e339")
anno.set_generator()
anno.generator.set_id("http://example.org/client1")
anno.generator.set_type("Software")
anno.generator.set_name("Code v2.1")
anno.generator.set_homepage("http://example.org/client1/homepage1")
anno.set_body("http://example.net/review1")
anno.set_target("http://example.com/restaurant1")
anno.to_json()

import dictdiffer                                                       

for i in dictdiffer.diff(r,anno.to_json()):
    print(i)