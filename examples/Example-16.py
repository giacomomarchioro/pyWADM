r= {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno16",
  "type": "Annotation",
  "rights": "https://creativecommons.org/publicdomain/zero/1.0/",
  "body": {
    "id": "http://example.net/review1",
    "rights": "http://creativecommons.org/licenses/by-nc/4.0/"
  },
  "target": "http://example.com/product1"
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno16")
anno.add_rights("https://creativecommons.org/publicdomain/zero/1.0/")
b1 = anno.set_body()
b1.set_id("http://example.net/review1")
b1.add_rights("http://creativecommons.org/licenses/by-nc/4.0/")
anno.set_target("http://example.com/product1")
anno.to_json()

import dictdiffer

for i in dictdiffer.diff(anno.to_json(),r):
    print(i)