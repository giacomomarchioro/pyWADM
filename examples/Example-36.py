# EXAMPLE 36: Rendering Software
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno36",
  "type": "Annotation",
  "body": "http://example.org/comment1",
  "target": {
    "source": "http://example.edu/article.pdf",
    "selector": "http://example.org/selectors/html-selector1",
    "renderedVia": {
      "id": "http://example.com/pdf-to-html-library",
      "type": "Software",
      "schema:softwareVersion": "2.5"
    }
  }
}

from wadm import WADM
anno = WADM.Annotation()
anno.set_id("http://example.org/anno36")
anno.set_body("http://example.org/comment1")
# We force the type to None
anno.set_target_specific_resource()
anno.target.type = None
anno.target.set_source("http://example.edu/article.pdf")
anno.target.set_selector("http://example.org/selectors/html-selector1")
sw = anno.target.add_renderedVia()
sw.set_id("http://example.com/pdf-to-html-library")
sw.set_softwareVersion( "2.5")
anno.to_json()