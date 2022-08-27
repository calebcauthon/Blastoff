from unittest import mock
import pytest
from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics
from libs.storyline import Storyline

def test_show_text():
  mockSerial = MagicMock()

  scene1 = basics.build_empty_scene_object()
  scene1.on("init").showText("Welcome")
  
  storyline = Storyline()
  storyline.serial = mockSerial
  storyline.setup({ "scenes": [scene1.config ]})
  storyline.start()

  assert mockSerial.showText.call_args_list == [mock.call("Welcome")]
