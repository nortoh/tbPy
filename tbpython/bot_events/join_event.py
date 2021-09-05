from ..enum_types import EventType
from ..bot_events import Event
from ..chat import User
from ..chat import Channel

class JoinEvent(Event):

    def __init__(self, user: User, channel: Channel):
        super().__init__(EventType.JOIN)
        self.__user__ = user
        self.__channel__ = channel

    def user(self):
        return self.__user__
    
    def channel(self):
        return self.__channel__

    