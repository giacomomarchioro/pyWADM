# EXAMPLE 41: Complete Example
r = {
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno38",
  "type": "Annotation",
  "motivation": "commenting",
  "creator": {
    "id": "http://example.org/user1",
    "type": "Person",
    "name": "A. Person",
    "nickname": "user1"
  },
  "created": "2015-10-13T13:00:00Z",
  "generator": {
    "id": "http://example.org/client1",
    "type": "Software",
    "name": "Code v2.1",
    "homepage": "http://example.org/homepage1"
  },
  "generated": "2015-10-14T15:13:28Z",
  "stylesheet": {
    "id": "http://example.org/stylesheet1",
    "type": "CssStylesheet"
  },
  "body": [
    {
      "type": "TextualBody",
      "purpose": "tagging",
      "value": "love"
    },
    {
      "type": "Choice",
      "items": [
        {
          "type": "TextualBody",
          "purpose": "describing",
          "value": "I really love this particular bit of text in this XML. No really.",
          "format": "text/plain",
          "language": "en",
          "creator": "http://example.org/user1"
        },
        {
          "type": "SpecificResource",
          "purpose": "describing",
          "source": {
            "id": "http://example.org/comment1",
            "type": "Audio",
            "format": "audio/mpeg",
            "language": "de",
            "creator": {
              "id": "http://example.org/user2",
              "type": "Person"
            }
          }
        }
      ]
    }
  ],
  "target": {
    "type": "SpecificResource",
    "styleClass": "mystyle",
    "source": "http://example.com/document1",
    "state": [
      {
        "type": "HttpRequestState",
        "value": "Accept: application/xml",
        "refinedBy": {
          "type": "TimeState",
          "sourceDate": "2015-09-25T12:00:00Z"
        }
      }
    ],
    "selector": {
      "type": "FragmentSelector",
      "value": "xpointer(/doc/body/section[2]/para[1])",
      "refinedBy": {
        "type": "TextPositionSelector",
        "start": 6,
        "end": 27
      }
    }
  }
}
from wadm import WADM

WADM.TYPES.append("Audio")
anno = WADM.Annotation()
anno.set_id("http://example.org/anno38")
anno.add_motivation("commenting")
creator  = anno.set_creator(WADM.Person())
creator.set_id("http://example.org/user1")
creator.set_name("A. Person")
creator.set_nickname("user1")
anno.set_created("2015-10-13T13:00:00Z")
sw = anno.set_generator(WADM.Software())
sw.set_id("http://example.org/client1")
sw.set_name("Code v2.1")
sw.set_homepage("http://example.org/homepage1")
anno.set_generated("2015-10-14T15:13:28Z")
css = anno.set_stylesheet()
css.set_type()
# TODO: check with the specs
css.id = "http://example.org/stylesheet1"
tb = anno.add_TextualBody()
tb.add_purpose("tagging")
tb.set_value("love")
choice = anno.add_ChoiceBody()
tb2 = choice.add_TextualBody_to_items()
tb2.add_purpose("describing")
tb2.set_value("I really love this particular bit of text in this XML. No really.")
tb2.set_format("text/plain")
tb2.add_language("en")
tb2.set_creator("http://example.org/user1")
sr = choice.add_SpecificResource_to_items()
sr.set_id("http://example.org/comment1")
sr.add_purpose("describing")
source = sr.set_source()
source.set_id("http://example.org/comment1")
source.set_type("Audio")
source.set_format("audio/mpeg")
source.add_language("de")
person = source.set_creator(WADM.Person())
person.set_id("http://example.org/user2")
tsr = anno.set_target_specific_resource()
tsr.set_styleClass("mystyle")
tsr.set_source("http://example.com/document1")
# Our command set the state if is one.
# rs = tsr.add_HttpRequestState()
rs = WADM.HttpRequestState()
rs.set_value("Accept: application/xml")
ts = rs.add_refinedBy(WADM.TimeState())
ts.add_sourceDate("2015-09-25T12:00:00Z")
fs = tsr.set_selector_as_FragmentSelector()
fs.set_value("xpointer(/doc/body/section[2]/para[1])")
tps = fs.add_refinedBy(WADM.TextPositionSelector())
tps.set_start(6)
tps.set_end(27)
# hack for using a list.
tsr.state = [rs]
anno.to_json()