from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock

def test_storyline_current_scene():
  scene1 = {
      "name": "scene1"
  }

  storyline = storylib.Storyline()
  storyline.setup({ "scenes": [scene1] })

  assert storyline.current_scene.name == "scene1"

def test_storyline_action():
  scene1 = {
    "name": "scene1",
    "advances": [
      {
        "on": "Bootup",
        "action": {
          "type": "next",
          "scene": "scene2"
        }
      }
      # on change knob to 5, go to scene 2
    ]
  }

  scene2 = {
    "name": "scene2"
  }

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({
    "scenes": [scene1, scene2]
  })

  storyline.start()
  storyline.event({
      "eventId": "1",
      "status": "Ended",
      "data": {
          "EventType": "Bootup"
      }
  })

  assert storyline.current_scene.name == "scene2"