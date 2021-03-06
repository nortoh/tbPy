from ..types.event_type import EventType
from ..events.event import Event

class ErrorEvent(Event):

    def __init__(self, error):
        super().__init__(EventType.ERROR)
        self.error = error
    