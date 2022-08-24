from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock

basicBootupEvent = {
    "eventId": "1",
    "status": "Ended",
    "data": {
        "EventType": "Bootup"
    }
}

def test_storyline_current_scene():
  scene1 = {
      "name": "scene1"
  }

  storyline = storylib.Storyline()
  storyline.setup({ "scenes": [scene1] })

  assert storyline.current_scene.name == "scene1"

def test_storyline_action_next_scene():
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
  storyline.event(basicBootupEvent)

  assert storyline.current_scene.name == "scene2"

def test_storyline_action_next_scene_init():
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
    ]
  }

  scene2 = {
    "name": "scene2",
    "init": [
      {
        "action": {
          "type": "serial",
          "message": "Scene 2 started"
        }
      }      
    ]
  }

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({
    "scenes": [scene1, scene2]
  })

  storyline.start()
  storyline.event(basicBootupEvent)

  mockSerial.send.assert_called_with("Scene 2 started")