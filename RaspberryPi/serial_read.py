#!/usr/bin/env python3
import serial
import time
import eventHandler

parameterValues = {
    "EventType": {
        "1": "Bootup",
        "2": "Heartbeat",
        "3": "ButtonPush",
        "4": "ValueChange",
        "5": "InputInit"
    }, 
    "Identification": {
        "1": "Slider"
    }
}

parameterNames = {
    "1": "Timestamp",
    "2": "Location",
    "3": "EventType",
    "4": "Value",
    "5": "Minimum",
    "6": "Maximum",
    "7": "Identification"
}

completedEvents = []
events = {}

def decode(line):
    try: 
        if (line.startswith("START")):
            parts = line.split("-")
            eventId = parts[1]
            event = {
                "eventId": eventId,
                "status": "Started",
                "data": {}
            }
            events[eventId] = event
        elif (line.startswith("END")):
            parts = line.split("-")
            eventId = parts[1]
            events[eventId]["status"] = "Ended"

            eventHandler.process(events[eventId])
            del events[eventId]

        elif (line.startswith("INFO")):
            parts = line.split("-")
            encodedParameter = parts[1]
            parameterParts = encodedParameter.split(":")
            eventId = parameterParts[0]
            attributeId = parameterParts[1]

            if (attributeId in parameterNames):
                name = parameterNames[attributeId]
            else:
                name = f"Unknown attribute: {attributeId}"

            value = parameterParts[2]

            if (name in parameterValues):
                if (value in parameterValues[name]):
                    value = parameterValues[name][value]
                else:
                    value = f"Unknown value for {name}: {value}"

            print(f"{name}={value}")
            events[eventId]["data"][name] = value
    except:
        print(f"unable to decode {line}")

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS5', 9600, timeout=1)
    ser.reset_input_buffer()

    lastValue = ""
    value = ""
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            decode(line)
