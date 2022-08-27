import random
from libs.scene import Scene
compare = {}


def build_empty_scene(name="scene1"):
  return {
    "name": name,
    "advances": [
    ]
}

def build_empty_scene_object(*args):
  return Scene(build_empty_scene(*args))

def build_on_event(eventType):
  return {
    "name": get_random_name(),
    "on": eventType,
    "active": True,
    "action": []
  }
def build_on_bootup(): 
  return build_on_event("Bootup")


def build_on_init(): 
  return build_on_event("init")

def build_on_button_push():
  return build_on_event("ButtonPush")

def build_on_value_change():
  return build_on_event("ValueChange")

def build_serial(message):
  return {
    "type": "serial",
    "message": message
  }

def build_show_text(message):
  return {
    "type": "show_text",
    "message": message
  }

def build_activate(id):
  return {
    "type": "activate",
    "action_id": id
  }

def build_variable(data_field, alias):
  return {
    "type": "variable",
    "field": data_field,
    "alias": alias
  }

def build_variable_increment(data_field, alias):
  return {
    "type": "variable_increment",
    "alias": alias
  }

def build_goto_scene(name):
  return {
    "type": "next",
    "scene": name
  }

EQUALS = "equals"
compare[EQUALS] = lambda a, b: b == a
GREATER_THAN = "greater_than"
compare[GREATER_THAN] = lambda a, b: b > a
LESS_THAN = "less_than"
compare[LESS_THAN] = lambda a, b: b < a

def build_simple_condition(name, value, operator):
  return {
    "requirements": [
      {
        "field": name,
        "value": value,
        "operator": operator
      }
    ]
  }

def build_equals_condition(name, value):
  return build_simple_condition(name, value, EQUALS)
def build_greater_than_condition(name, value):
  return build_simple_condition(name, value, GREATER_THAN)
def build_less_than_condition(name, value):
  return build_simple_condition(name, value, LESS_THAN)


def build_multiple_condition(operations):
  requirements = []
  for item in operations:
    name, value, operator = tuple(item)
    requirements.append({
      "field": name,
      "value": value,
      "operator": operator
    })
  return {
    "requirements": requirements
  }

def get_random_name():
  letters = "abcqwerasdfzxcv"
  return ''.join(random.choice(letters) for i in range(10))