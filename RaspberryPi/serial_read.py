#!/usr/bin/env python3
import serial
import time
from libs import decoder
from events import parameterNames, parameterValues
import events.parameter_names
from libs import storyline as storylib

events = {}
scene1 = {
    "name": "scene1",
    "advances": [
        {
            "on": "Bootup",
            "action": {
                "type": "next",
                "scene": "scene2"
            }
        },
        {
            "on": "ButtonPush",
            "action": {
                "type": "next",
                "scene": "scene2"
            }
        }
    ]
}

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
