#!/usr/bin/env python3
from libs.debugging.logging import piprint, arduinoprint
import serial
import time
from libs import decoder
from events import parameterNames, parameterValues
import events.parameter_names
from libs import storyline as storylib
from libs.scene_templates import basics

knobId = 2 

settings_count = 3
max_value = 1024
knobMap = {
    "Comms": { "from": str(max_value / settings_count * 0), "to": str(max_value / settings_count * 1), "value": "Comms" },
    "Engine": { "from": str(max_value / settings_count * 1), "to": str(max_value / settings_count * 2), "value": "Engine" },
    "Nav": { "from": str(max_value / settings_count * 2), "to": str(max_value / settings_count * 3), "value": "Nav" },
}

events = {}
scene = basics.build_empty_scene_object()
scene.on("Bootup").showText("Lets get started. Set engine to idle ")
scene.on("ValueChange", basics.build_equals_condition("Identification", "Knob")).saveAs("KnobValue")
scene.on("ValueChange").showText("Engine: __KnobValue__ RPM")
#scene.on("ValueChange", basics.build_simple_condition(
#    "__KnobValue__", knobMap["Engine"]["from"], basics.LESS_THAN
#)).showText(f"Too small! Engine @ __KnobValue__RPM. Target: {knobMap['Engine']['from']}RPM")
#scene.on("ValueChange", basics.build_simple_condition(
#    "KnobValue", knobMap["Engine"]["to"], basics.GREATER_THAN
#)).showText(f"Too big! Engine @ __KnobValue__RPM. Target: {knobMap['Engine']['to']}RPM")
#scene.on("ValueChange", basics.build_multiple_condition([
#    ["KnobValue", knobMap["Engine"]["from"], basics.GREATER_THAN],
#    ["KnobValue", knobMap["Engine"]["to"], basics.LESS_THAN]
#])).showText("Good job!")


class SerialWrapper:
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyS5', 115200, timeout=1)
        except serial.serialutil.SerialException:
            piprint("Could not open serial port")
            raise
        self.ser.reset_input_buffer()
        self.lines = []
    
    def buffer_filled(self):
        return len(self.lines) > 0

    def send(self, message):
        self.lines.append(message)
        return self

    def showText(self, message):
        self.lines.append(message)
        return self

    def ser(self):
        self.ser

    def immediately(self):
        self.write()

    def read_all_from_serial(self):
        in_waiting = storyline.serial.ser.in_waiting > 0
        while in_waiting:
            line = storyline.serial.ser.readline().decode('utf-8', 'ignore').rstrip()
            arduinoprint(line)
            decoder.decode(line, events, parameterNames, parameterValues, storyline)

            in_waiting = storyline.serial.ser.in_waiting > 0


    def write(self):
        message = len(self.lines) > 0 and self.lines.pop(-1)
        while (message):
            self.ser.write(bytes(message, encoding='utf-8'))
            piprint(f"Wrote {bytes(message, encoding='utf-8')}")
            message = len(self.lines) > 0 and self.lines.pop(-1)


storyline = storylib.Storyline()
storyline.serial = SerialWrapper()
storyline.setup({
    "scenes": [scene.config]
})



if __name__ == '__main__':
    storyline.start()

    lastValue = ""
    value = ""
    while True:
        if storyline.serial.ser.in_waiting > 0:
            line = storyline.serial.ser.readline().decode('utf-8', 'ignore').rstrip()
            arduinoprint(line)
            decoder.decode(line, events, parameterNames, parameterValues, storyline)
        elif(storyline.serial.buffer_filled()):
            piprint("Writing buffer to serial port")
            storyline.serial.write()
            #piprint("sleeping for 1 second")
            #time.sleep(1)
