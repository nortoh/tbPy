from ..bot_events import Event
from ..enum_types import EventType
from ..chat import Channel
import string

class RoomStateEvent(Event):

    def __init__(self, channel: Channel):
        super().__init__(EventType.ROOMSTATE)
        self.__channel__ = channel

    def channel(self):
        return self.__channel__
