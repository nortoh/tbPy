from enum_types.event_type import EventType
from bot_events.event import Event

class StartUpEvent(Event):

    def __init__(self):
        super().__init__(EventType.STARTUP)
    