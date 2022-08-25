import libs.scene_templates

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
    
  def on(self, eventType):
    advance = Advance(libs.scene_templates.basics.build_on_event(eventType))
    self.advances().append(advance.config)
    return advance

class Advance:
  def __init__(self, config):
    self.config = config

  def saveAs(self, name):
    action = libs.scene_templates.basics.build_variable("Value", "SliderValue")
    self.config["action"].append(action)

  def sendSerial(self, message):
    action = libs.scene_templates.basics.build_serial(message)
    self.config["action"].append(action)
