from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock

def test_storyline_action():
  scene1 = {
    "name": "scene1",
    "init": [
      {
        "action": {
          "type": "serial",
          "message": "Scene 1 started"
        }
      }      
    ]
  }

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1] })

  storyline.start()
  mockSerial.send.assert_called_with("Scene 1 started")
