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

