import libs.scene_templates
from libs.advance import Advance

class Scene:
  def __init__(self, config):
    self.config = config
    self.name = config["name"]
    self.serial = None

  def getInit(self):
    if ("init" in self.config):
      return self.config["init"]
    else:
      return {}

  def advances(self):
    if ("advances" not in self.config):
      self.config["advances"] = {}

    return self.config["advances"]
    
  def on(self, eventType, condition=None):
    advance = Advance(libs.scene_templates.basics.build_on_event(eventType))
    if (condition):
      advance.addCondition(condition)
    advance.serial = self.serial
    self.advances().append(advance.config)
    return advance
