class Scene:
  def __init__(self, config):
    self.config = config
    self.name = config["name"]

  def getInit(self):
    if ("init" in self.config):
      return self.config["init"]
    else:
      return {}

  def advances(self):
    if ("advances" in self.config):
      return self.config["advances"]
    else:
      return {}