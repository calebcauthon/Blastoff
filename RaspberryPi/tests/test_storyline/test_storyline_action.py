from libs import storyline as storylib
from unittest.mock import MagicMock
from libs.scene_templates import basics

def test_storyline_action():
  scene1 = basics.build_empty_scene()
  on_bootup = basics.build_on_bootup()
  serial_action = basics.build_serial("1-Show this text")
  on_bootup["action"] = serial_action
  scene1["advances"].append(on_bootup)

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1] })

  storyline.start()
  storyline.event({
      "eventId": "1",
      "status": "Ended",
      "data": {
          "EventType": "Bootup"
      }
  })

  mockSerial.send.assert_called_with("1-Show this text")

def test_storyline_process():
  scene1 = basics.build_empty_scene()
  on_bootup = basics.build_on_bootup()
  serial_action = basics.build_serial("1-Show this text")
  on_bootup["action"] = serial_action
  scene1["advances"].append(on_bootup)

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1] })

  storyline.start()
  storyline.process({
      "eventId": "1",
      "status": "Ended",
      "data": {
          "EventType": "Bootup"
      }
  })

  mockSerial.send.assert_called_with("1-Show this text")