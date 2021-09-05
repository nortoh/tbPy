from ..enum_types import EventType
from ..bot_events import Event
from ..chat import User
from ..chat import Channel

class PartEvent(Event):

    def __init__(self, user: User, channel: Channel):
        super().__init__(EventType.PART)
        self.__user = user
        self.__channel = channel

    def user(self):
        return self.__user
    
    def channel(self):
        return self.__channel

    