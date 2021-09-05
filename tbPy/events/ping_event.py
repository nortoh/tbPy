from ..types import EventType
from ..events import Event

class PingEvent(Event):

    def __init__(self):
        super().__init__(EventType.PING)
    