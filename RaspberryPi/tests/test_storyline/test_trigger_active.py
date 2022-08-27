from unittest import mock
import pytest
from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics
from libs.storyline import Storyline

def test_storyline_inactive():
  scene1 = basics.build_empty_scene()
  scene2 = basics.build_empty_scene("scene2")
  on_init = basics.build_on_init()
  on_init["action"].append(basics.build_goto_scene("scene2"))
  on_init["active"] = False
  scene1["advances"].append(on_init)


  storyline = Storyline()
  storyline.setup({
    "scenes": [scene1, scene2]
  })

  storyline.start()

  assert storyline.current_scene.name == "scene1"
 