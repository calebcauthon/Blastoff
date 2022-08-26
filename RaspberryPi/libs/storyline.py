from libs import scene as scenelib
from libs.scene_templates import basics
import time

class Storyline:
  def __init__(self):
    self.variables = {}
    self.serial = None

  def setup(self, config):
    self.scenes = []

    for scene in config["scenes"]:
      self.scenes.append(scenelib.Scene(scene))

    self.current_scene = self.scenes[0]
    self.current_scene.serial = self.serial
    print(f"storyline.serial={self.serial}")


  def start(self):
    self.event({
      "data": {
        "EventType": "init"
      }
    })

  def gotoScene(self, sceneName):
    print(f"gotoScene('{sceneName}')")
    for scene in self.scenes:
      if scene.name == sceneName:
        self.current_scene = scene
        self.current_scene.serial = self.serial
        print(f"self.start() while current scene is '{self.current_scene.name}'")
        self.start()

  def process(self, eventInfo):
    return self.event(eventInfo)

  def event(self, eventInfo):
    for directive in self.current_scene.advances():
      if (directive["active"] == True and directive["on"] == eventInfo["data"]["EventType"] and ("condition" not in directive or self.isConditionMet(directive["condition"], eventInfo["data"]))):
        for action in directive["action"]:
          if (action["type"] == "serial"):
            self.executeSerialDirective(action)
          if (action["type"] == "show_text"):
            self.executeShowTextDirective(action)
          elif (action["type"] == "next"): 
            sceneName = action["scene"] 
            self.gotoScene(sceneName)
          elif (action["type"] == "variable"):
            alias = action["alias"]
            data_field = action["field"]
            value = eventInfo["data"][data_field]
            self.variables[alias] = value
          elif (action["type"] == "variable_increment"):
            alias = action["alias"]
            if alias not in self.variables:
              self.variables[alias] = 0
            self.variables[alias] = self.variables[alias] + 1
          elif (action["type"] == "activate"):
            for scene in self.scenes:
              for advance in scene.advances():
                if (advance["name"] == action["action_id"]):
                  advance["active"] = True

  def executeSerialDirective(self, action):
    message = self.interpolate(action["message"])
    self.serial.send(message)

  def executeShowTextDirective(self, action):
    print(f"about to interpolate {action['message']} using {self.variables}")
    message = self.interpolate(action["message"])
    self.serial.showText(message)

  def isConditionMet(self, condition, eventData):
    for requirements in condition["requirements"]:
      field = requirements["field"]
      expected_value = requirements["value"]
      operator = requirements["operator"]
      
      if (operator in basics.compare):
        print(f"operator={operator}, field={field}, eventData={eventData}, expected_value={expected_value}")
        if (field in eventData):
          test_value = eventData[field]
        else:
          test_value = self.interpolate(field)
          print(f"test_value={test_value}")
        if basics.compare[operator](expected_value, test_value) == False:
          return False

    return True
  
  def interpolate(self, text):
    for alias, value in self.variables.items():
      text = text.replace(f"__{alias}__", str(value))

    return text