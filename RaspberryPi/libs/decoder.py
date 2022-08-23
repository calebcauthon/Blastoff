def decode(line, events, parameterNames, parameterValues, eventHandler):
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
    except Exception as e:
        print(f"unable to decode {line}: {e}")

