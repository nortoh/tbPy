from ..enum_types import EventType
from ..bot_events import Event

class StartUpEvent(Event):

    def __init__(self):
        super().__init__(EventType.STARTUP)
    