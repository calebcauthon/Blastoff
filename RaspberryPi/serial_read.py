#!/usr/bin/env python3
import serial
import time
import decoder
from events import parameterNames, parameterValues
import events.parameter_names

events = {}

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS5', 9600, timeout=1)
    ser.reset_input_buffer()

    lastValue = ""
    value = ""
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            decoder.decode(line, events, parameterNames, parameterValues)
