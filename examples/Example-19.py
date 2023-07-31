# EXAMPLE 19: Selectors
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno19",
  "type": "Annotation",
  "body": {
    "source": "http://example.org/page1",
    "selector": "http://example.org/paraselector1"
  },
  "target": {
    "source": "http://example.com/dataset1",
    "selector": "http://example.org/dataselector1"
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno19")
anno.set_body()
anno.body.set_source("http://example.org/page1")
anno.body.set_selector("http://example.org/paraselector1")
anno.set_target()
anno.target.set_source("http://example.com/dataset1")
anno.target.set_selector("http://example.org/dataselector1")
anno.to_json()