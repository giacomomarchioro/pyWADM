r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno11",
  "type": "Annotation",
  "creator": "http://example.org/user1",
  "created": "2015-01-28T12:00:00Z",
  "modified": "2015-01-29T09:00:00Z",
  "generator": "http://example.org/client1",
  "generated": "2015-02-04T12:00:00Z",
  "body": {
    "id": "http://example.net/review1",
    "creator": "http://example.net/user2",
    "created": "2014-06-02T17:00:00Z"
  },
  "target": "http://example.com/restaurant1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno11")
anno.set_creator("http://example.org/user1")
anno.set_created("2015-01-28T12:00:00Z")
anno.set_modified("2015-01-29T09:00:00Z")
anno.set_generator("http://example.org/client1")
anno.set_generated("2015-02-04T12:00:00Z")
anno.set_body()
anno.body.set_id("http://example.net/review1")
anno.body.set_creator("http://example.net/user2")
anno.body.set_created("2014-06-02T17:00:00Z")
anno.set_target("http://example.com/restaurant1")
anno.to_json()