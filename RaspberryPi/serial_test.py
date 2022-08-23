#!/usr/bin/env python3
import serial
import time

eventNames = {
    "1": "Bootup",
    "2": "Heartbeat"
}

parameterNames = {
    "1": "Timestamp",
    "2": "Location"
}

completedEvents = []
events = {}

def decode(line):
    if (line.startswith("START")):
        parts = line.split("-")
        eventId = parts[1]
        event = {
            "name": eventNames[eventId],
            "status": "Started",
            "data": {}
        }
        events[eventId] = event
    elif (line.startswith("END")):
        parts = line.split("-")
        eventId = parts[1]
        events[eventId]["status"] = "Ended"

        completedEvents.append(events[eventId])
        del events[eventId]

    elif (line.startswith("INFO")):
        parts = line.split("-")
        encodedParameter = parts[1]
        parameterParts = encodedParameter.split(":")
        eventId = parameterParts[0]
        name = parameterNames[parameterParts[1]]
        value = parameterParts[2]

        events[eventId]["data"][name] = value



if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    lastValue = ""
    value = ""
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print("Decoding...\n")
            print(line)
            decode(line)
            #print("Events:")
            #print(events)

            #print("CompletedEvents:")
            #print(completedEvents)
            if (line.startswith("END")):
                ser.write(b"912345")
                print("Wrote a 9")
                time.sleep(1)
