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
    if ("advances" not in self.config):
      self.config["advances"] = {}

    return self.config["advances"]
    

  def when(self, advance, action):
    if advance not in self.advances():
      self.advances().append(advance)

    advance["action"].append(action)