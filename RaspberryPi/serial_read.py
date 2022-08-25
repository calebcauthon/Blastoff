#!/usr/bin/env python3
from cgitb import text
import serial
import time
from libs import decoder
from events import parameterNames, parameterValues
import events.parameter_names
from libs import storyline as storylib
from libs.scene_templates import basics

events = {}
opening_scene = basics.build_empty_scene()
opening_scene["name"] = "Opening Scene"

text1 = basics.build_on_init()
text1["action"].append(arduinoShowOnScreen("Welcome! Press a button to continue."))

text2 = basics.build_on_button_push()
text2["action"].append(arduinoShowOnScreen("We've never had a captain as handsome as you."))
text2["action"].append(basics.build_enable_advance("text3"))

text3 = basics.build_on_button_push("text3")
text3["enabled"] = False
text3["action"].append(arduinoShowOnScreen("Let's get to that planet!"))


goto_scene_2 = basics.build_goto_scene("scene2")
on_bootup = basics.build_on_bootup()
on_bootup["action"] = goto_scene_2
on_button_push = basics.build_on_button_push()
on_button_push["action"] = goto_scene_2
scene1["advances"].append(on_bootup)
scene1["advances"].append(on_button_push)

scene2 = {
    "name": "scene2",
    "advances": [
        {
            "on": "ButtonPush",
            "action": {
                "type": "serial",
                "message": "button was pushed!\n"
            }
        }
    ],
    "init": [
        {
            "action": {
                "type": "serial",
                "message": "Scene 2 started\n"
            }
        }      
    ]
}

class SerialWrapper:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS5', 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.lines = []
    
    def send(self, message):
        self.lines.append(message)

    def ser(self):
        self.ser

    def write(self):
        message = len(self.lines) > 0 and self.lines.pop(-1)
        while (message):
            self.ser.write(bytes(message, encoding='utf-8'))
            print(f"Wrote {bytes(message, encoding='utf-8')}")
            message = len(self.lines) > 0 and self.lines.pop(-1)


storyline = storylib.Storyline()
storyline.serial = SerialWrapper()
storyline.setup({
    "scenes": [scene1, scene2]
})



if __name__ == '__main__':
    storyline.start()

    lastValue = ""
    value = ""
    while True:
        if storyline.serial.ser.in_waiting > 0:
            print("reading.")
            line = storyline.serial.ser.readline().decode('utf-8', 'ignore').rstrip()
            print(line)
            print("\n")
            decoder.decode(line, events, parameterNames, parameterValues, storyline)
        else:
            storyline.serial.write()
