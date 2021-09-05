from ..types.event_type import EventType
from ..events.event import Event

class NewdayEvent(Event):

    def __init__(self):
        super().__init__(EventType.NEWDAY)
    