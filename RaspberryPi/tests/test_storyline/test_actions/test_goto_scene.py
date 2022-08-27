from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics

basicBootupEvent = {
    "eventId": "1",
    "status": "Ended",
    "data": {
        "EventType": "Bootup"
    }
}

def test_storyline_current_scene():
  scene1 = basics.build_empty_scene()
  storyline = storylib.Storyline()
  storyline.setup({ "scenes": [scene1] })

  assert storyline.current_scene.name == "scene1"

def test_storyline_action_next_scene():
  scene1 = basics.build_empty_scene()
  next_scene = basics.build_goto_scene("scene2")
  on_bootup = basics.build_on_bootup()
  on_bootup["action"].append(next_scene)
  scene1["advances"].append(on_bootup)

  scene2 = basics.build_empty_scene()
  scene2["name"] = "scene2"

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
  scene1 = basics.build_empty_scene()
  on_bootup = basics.build_on_bootup()
  goto_scene = basics.build_goto_scene("scene2")
  on_bootup["action"].append(goto_scene)
  scene1["advances"].append(on_bootup)
   
  scene2 = basics.build_empty_scene()
  scene2["name"] = "scene2"
  on_init = basics.build_on_init()
  serial_action = basics.build_serial("Scene 2 started")
  on_init["action"].append(serial_action)
  scene2["advances"].append(on_init)

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({
    "scenes": [scene1, scene2]
  })

  storyline.start()
  storyline.event(basicBootupEvent)

  mockSerial.send.assert_called_with("Scene 2 started")