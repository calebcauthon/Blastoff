import libs.scene_templates

class Advance:
  def __init__(self, config):
    self.config = config
    self.serial = None

  def addCondition(self, condition):
    self.config["condition"] = condition

  def saveAs(self, name):
    action = libs.scene_templates.basics.build_variable("Value", name)
    self.config["action"].append(action)

  def sendSerial(self, message):
    action = libs.scene_templates.basics.build_serial(message)
    self.config["action"].append(action)

  def showText(self, message):
    action = libs.scene_templates.basics.build_show_text(message)
    self.config["action"].append(action)
