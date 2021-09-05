from ..bot_events.event import Event
from ..enum_types.event_type import EventType

from ..chat.user import User
from ..chat.channel import Channel
from ..chat.tag import Tag

class ClearMessageEvent(Event):

    def __init__(self, user: User, channel: Channel, tag: Tag, deleted_message):
        super().__init__(EventType.CLEARMSG)
        self.__user__ = user
        self.__channel__ = channel
        self.__tag__ = tag
        self.__deleted_message__ = deleted_message

    def user(self):
        return self.__user__
    
    def channel(self):
        return self.__channel__

    def tag(self):
        return self.__tag__
    
    def deleted_message(self):
        return self.__deleted_message__