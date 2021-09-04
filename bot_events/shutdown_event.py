from enum_types.event_type import EventType
from bot_events.event import Event

class ShutdownEvent(Event):

    def __init__(self):
        super().__init__(EventType.SHUTDOWN)
    