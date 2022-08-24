class Scene:
  def __init__(self, config):
    self.config = config
    self.name = config["name"]

  def advances(self):
    if ("advances" in self.config):
      return self.config["advances"]
    else:
      return {}