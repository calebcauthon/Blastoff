from libs import storyline as storylib
from unittest.mock import MagicMock

def test_storyline():
  scene1 = {
    "init": [
      
    ],
    "advances": [
      {
        "on": "Bootup",
        "action": { "serial": "1-Show this text" }
      }
      # on change knob to 5, go to scene 2
    ],
    "twists": {
      # on too much time passes, perform x (but stay on this scene)
    }
  }

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup(scene1)

  storyline.start()
  storyline.event({
      "eventId": "1",
      "status": "Ended",
      "data": {
          "EventType": "Bootup"
      }
  })

  mockSerial.send.assert_called_with("1-Show this text")