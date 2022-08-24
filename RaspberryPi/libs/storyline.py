class Storyline:
  def setup(self, scene):
    self.scene = scene

  def start(self):
    pass

  def event(self, eventInfo):
    for directive in self.scene["advances"]:
      if (directive["on"] == eventInfo["data"]["EventType"]):
        if (directive["action"]["type"] == "serial"):
          message = directive["action"]["message"]
          self.serial.send(message)
    