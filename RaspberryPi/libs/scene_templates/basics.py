compare = {}


def build_empty_scene():
  return {
  "name": "scene1",
  "advances": [
  ]
}

def build_on_bootup(): 
  return {
    "on": "Bootup",
    "action": {}
  }

def build_on_init(): 
  return {
    "on": "init",
    "action": {}
  }

def build_on_button_push():
  return {
    "on": "ButtonPush",
    "action": {}
  }

def build_serial(message):
  return {
    "type": "serial",
    "message": message
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
  return build_simple_condition(name, value, EQUALS);
def build_greater_than_condition(name, value):
  return build_simple_condition(name, value, GREATER_THAN);
def build_less_than_condition(name, value):
  return build_simple_condition(name, value, LESS_THAN);
