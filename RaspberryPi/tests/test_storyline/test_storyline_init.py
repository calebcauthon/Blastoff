from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics

def test_storyline_first_scene_init():
  scene1 = basics.build_empty_scene()
  on_init = basics.build_on_init()
  serial_action = basics.build_serial("Scene 1 started")
  on_init["action"].append(serial_action)
  scene1["advances"].append(on_init)

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1] })

  storyline.start()
  mockSerial.send.assert_called_with("Scene 1 started")
