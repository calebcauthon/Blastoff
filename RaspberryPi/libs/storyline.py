class Storyline:
  def setup(self, scene):
    pass

  def start(self):
    pass

  def event(self, eventInfo):
    if (eventInfo["data"]["EventType"] == "Bootup"):
      message = "1-Show this text"
      self.serial.send(message)
    