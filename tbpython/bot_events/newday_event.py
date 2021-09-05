from ..enum_types.event_type import EventType
from ..bot_events.event import Event

class NewdayEvent(Event):

    def __init__(self):
        super().__init__(EventType.NEWDAY)
    