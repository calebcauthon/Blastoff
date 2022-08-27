from unittest import mock
import pytest
from libs import storyline as storylib
from libs import scene as scenelib
from unittest.mock import MagicMock
from libs.scene_templates import basics
from libs.storyline import Storyline

def test_activate_trigger_action():
  on_button_push = basics.build_on_button_push()

  scene1 = basics.build_empty_scene()
  on_init = basics.build_on_init()
  activate_button_push = basics.build_activate(on_button_push["name"])
  on_init["action"].append(activate_button_push)

  on_button_push["action"].append(basics.build_goto_scene("scene2"))
  on_button_push["active"] = False

  scene1["advances"].append(on_init)
  scene1["advances"].append(on_button_push)

  scene2 = basics.build_empty_scene("scene2")

  on_init2 = basics.build_on_init()
  on_init2["active"] = False
  on_init2["action"].append(basics.build_goto_scene("scene3"))
  scene2["advances"].append(on_init2)

  scene3 = basics.build_empty_scene("scene3")


  storyline = Storyline()
  storyline.setup({
    "scenes": [scene1, scene2, scene3]
  })

  storyline.start()
  storyline.process({
    "data": {
      "EventType": "ButtonPush"
    }
  })

  print(storyline.scenes[0].advances())

  assert storyline.current_scene.name == "scene2"
