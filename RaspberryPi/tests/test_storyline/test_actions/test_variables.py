from unittest import mock
import pytest
from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics
from libs.storyline import Storyline

def test_storyline_variable_storage():
  scene1 = basics.build_empty_scene()
  on_slider = basics.build_on_value_change()
  variable_action = basics.build_variable("Value", "SliderValue")
  serial_action = basics.build_serial("Slider value was last seen at __SliderValue__")
  on_slider["action"].append(variable_action)
  on_slider["action"].append(serial_action)
  scene1["advances"].append(on_slider)

  print(f"{scene1}")

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1] })

  storyline.start()
  storyline.event({
    "eventId": "1",
    "status": "Ended",
    "data": {
      "EventType": "ValueChange",
      "Value": "730"
    }
  })

  assert mockSerial.send.call_args_list == [mock.call("Slider value was last seen at 730")]

def test_storyline_variable_increment():
  scene1 = basics.build_empty_scene()
  on_slider = basics.build_on_value_change()
  variable_action = basics.build_variable_increment("Value", "SliderCount")
  serial_action = basics.build_serial("Slider has been tapped __SliderCount__ times")
  on_slider["action"].append(variable_action)
  on_slider["action"].append(serial_action)
  scene1["advances"].append(on_slider)

  print(f"{scene1}")

  mockSerial = MagicMock()

  storyline = storylib.Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1] })

  storyline.start()
  storyline.event({
    "eventId": "1",
    "status": "Ended",
    "data": {
      "EventType": "ValueChange",
      "Value": "730"
    }
  })

  storyline.event({
    "eventId": "1",
    "status": "Ended",
    "data": {
      "EventType": "ValueChange",
      "Value": "731"
    }
  })

  assert mockSerial.send.call_args_list == [mock.call("Slider has been tapped 1 times"), mock.call("Slider has been tapped 2 times")]