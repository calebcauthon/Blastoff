from libs import scene as scenelib

class Storyline:

  def setup(self, config):
    self.scenes = []

    for scene in config["scenes"]:
      self.scenes.append(scenelib.Scene(scene))

    self.current_scene = self.scenes[0]


  def start(self):
    for directive in self.current_scene.getInit():
      if ("action" in directive):
        actionType = directive["action"]["type"]
        if (directive["action"]["type"] == "serial"):
          self.executeSerialDirective(directive)

  def gotoScene(self, sceneName):
    for scene in self.scenes:
      if scene.name == sceneName:
        self.current_scene = scene

  def event(self, eventInfo):
    for directive in self.current_scene.advances():
      if (directive["on"] == eventInfo["data"]["EventType"]):
        if (directive["action"]["type"] == "serial"):
          self.executeSerialDirective(directive)
        elif (directive["action"]["type"] == "next"): 
          sceneName = directive["action"]["scene"] 
          self.gotoScene(sceneName)

  def executeSerialDirective(self, directive):
    message = directive["action"]["message"]
    self.serial.send(message)

    