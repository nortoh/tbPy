from ..enum_types import EventType
from ..bot_events import Event

class ErrorEvent(Event):

    def __init__(self, error):
        super().__init__(EventType.ERROR)
        self.error = error
    