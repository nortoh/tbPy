from ..types import EventType
from ..events import Event

class StartUpEvent(Event):

    def __init__(self):
        super().__init__(EventType.STARTUP)
    