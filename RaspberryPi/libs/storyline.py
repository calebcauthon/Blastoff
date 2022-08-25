from libs import scene as scenelib
from libs.scene_templates import basics
import time

class Storyline:
  def __init__(self):
    self.variables = {}

  def setup(self, config):
    self.scenes = []

    for scene in config["scenes"]:
      self.scenes.append(scenelib.Scene(scene))

    self.current_scene = self.scenes[0]


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


  def executeSerialDirective(self, action):
    message = action["message"]
    for alias, value in self.variables.items():
      message = message.replace(f"__{alias}__", str(value))
    self.serial.send(message)
    print(f"sending serial message: {message}")

  def isConditionMet(self, condition, eventData):
    for requirements in condition["requirements"]:
      field = requirements["field"]
      expected_value = requirements["value"]
      operator = requirements["operator"]
      
      if (operator in basics.compare):
        if basics.compare[operator](expected_value, eventData[field]) == False:
          return False

    return True