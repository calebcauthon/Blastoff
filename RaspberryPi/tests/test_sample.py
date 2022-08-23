from libs import decoder
from events import parameterNames, parameterValues
from unittest.mock import MagicMock


def test_decode_event():
    eventHandler = MagicMock()
    eventHandler.process = MagicMock()

    lines = [
        "START-1",
        "END-1",
    ]
    events = {}
    for line in lines:
        decoder.decode(line, events, parameterNames, parameterValues, eventHandler)

    eventHandler.process.assert_called_with({
        "eventId": "1",
        "status": "Ended",
        "data": {}
    })
