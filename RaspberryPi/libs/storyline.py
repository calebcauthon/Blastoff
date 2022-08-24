from libs import scene as scenelib
import time

class Storyline:

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
      if (directive["on"] == eventInfo["data"]["EventType"]):
        print(f"Received event with recognized type: {eventInfo} \n   which triggers directive: {directive}")
        if (directive["action"]["type"] == "serial"):
          self.executeSerialDirective(directive)
        elif (directive["action"]["type"] == "next"): 
          sceneName = directive["action"]["scene"] 
          self.gotoScene(sceneName)

  def executeSerialDirective(self, directive):
    print(f"executeSerialDirective({directive})")
    message = directive["action"]["message"]
    self.serial.send(message)
    print(f"sending serial message: {message}")

    