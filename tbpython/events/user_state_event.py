from ..events import Event
from ..types import EventType
from ..chat import Channel
from ..chat import Tag
import string

class UserStateEvent(Event):

    def __init__(self, channel: Channel, tag: Tag):
        super().__init__(EventType.USERSTATE)
        self.__channel__ = channel
        self.__tag__ = tag
    
    def channel(self):
        return self.__channel__

    def tag(self):
        return self.__tag__
