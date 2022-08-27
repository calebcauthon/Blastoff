from distutils.command.build import build


def decode(line, events, parameterNames, parameterValues, eventHandler):
    if (line.startswith("START")):
        parts = line.split("-")
        eventId = parts[1]
        event = build_empty_event(eventId)
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
                value = f"Unknown value for {name}: {value}\n"

        print(f"eventId={eventId}, name={name}, value={value}")
        
        if (eventId not in events):
            events[eventId] = build_empty_event(eventId)

        events[eventId]["data"][name] = value

def build_empty_event(eventId):
    return {
        "eventId": eventId,
        "status": "Started",
        "data": {}
    }
