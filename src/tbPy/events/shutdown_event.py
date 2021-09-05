from ..types import EventType
from ..events import Event

class ShutdownEvent(Event):

    def __init__(self):
        super().__init__(EventType.SHUTDOWN)
    