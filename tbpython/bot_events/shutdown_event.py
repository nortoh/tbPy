from ..enum_types import EventType
from ..bot_events import Event

class ShutdownEvent(Event):

    def __init__(self):
        super().__init__(EventType.SHUTDOWN)
    