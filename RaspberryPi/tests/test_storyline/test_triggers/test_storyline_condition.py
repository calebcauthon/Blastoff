from unittest import mock
import pytest
from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics
from libs.storyline import Storyline


@pytest.mark.parametrize("data,condition,expected_call_list", [
  (
    { "the value": "250" },
    basics.build_equals_condition("the value", "250"),
    [mock.call("the text")]
  ),
  (
    { "the value": "251" },
    basics.build_equals_condition("the value", "250"),
    []
  ),
  (
    { "the value": "249" },
    basics.build_greater_than_condition("the value", "250"),
    []
  ),
  (
    { "the value": "251" },
    basics.build_greater_than_condition("the value", "250"),
    [mock.call("the text")]
  ),
  (
    { "the value": "249" },
    basics.build_less_than_condition("the value", "250"),
    [mock.call("the text")]
  ),
  (
    { "the value": "251" },
    basics.build_less_than_condition("the value", "250"),
    []
  ),
  (
    { "the value": "249" },
    basics.build_multiple_condition([
      ["the value", "250", basics.GREATER_THAN],
      ["the value", "252", basics.LESS_THAN]
    ]),
    []
  ),
  (
    { "the value": "251" },
    basics.build_multiple_condition([
      ["the value", "250", basics.GREATER_THAN],
      ["the value", "252", basics.LESS_THAN]
    ]),
    [mock.call("the text")]
  )
])
def test_condition_true(data, condition, expected_call_list):
  scene1 = basics.build_empty_scene_object()
  scene1.on("ButtonPush", condition).sendSerial("the text")

  mockSerial = MagicMock()
  storyline = Storyline()
  storyline.serial = mockSerial
  storyline.setup({
    "scenes": [scene1.config]
  })

  storyline.start()
  eventData = {
    "EventType": "ButtonPush",
  }
  storyline.process({
    "data": {**eventData, **data}
  })
  

  assert mockSerial.send.call_args_list == expected_call_list
 
def test_multiple_conditions():
  condition1 = basics.build_greater_than_condition("the value", "250")
  condition2 = basics.build_less_than_condition("the value", "255")

  condition1["requirements"] = condition1["requirements"] + condition2["requirements"]  

  scene1 = basics.build_empty_scene()
  on_button = basics.build_on_button_push()
  serial_action = basics.build_serial("the text")
  on_button["action"].append(serial_action)
  scene1["advances"].append(on_button)

  on_button["condition"] = condition1

  mockSerial = MagicMock()
  storyline = Storyline()
  storyline.serial = mockSerial
  storyline.setup({
    "scenes": [scene1]
  })

  storyline.start()
  eventData = {
    "EventType": "ButtonPush",
  }
  data = { "the value": "256" }
  storyline.process({
    "data": {**eventData, **data}
  })
  

  assert mockSerial.send.call_args_list == []
 

def test_variable_in_condition():
  data = { "Value": "250" }
  condition = basics.build_equals_condition("__savedValue__", "250")
  expected_call_list = [mock.call("the text")]
  scene1 = basics.build_empty_scene_object()
  scene1.on("ButtonPush").saveAs("savedValue")
  scene1.on("ButtonPush", condition).sendSerial("the text")

  mockSerial = MagicMock()
  storyline = Storyline()
  storyline.serial = mockSerial
  storyline.setup({
    "scenes": [scene1.config]
  })

  storyline.start()
  eventData = {
    "EventType": "ButtonPush",
  }
  storyline.process({
    "data": {**eventData, **data}
  })
  

  assert mockSerial.send.call_args_list == expected_call_list