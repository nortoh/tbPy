from ..bot_events import Event
from ..enum_types import EventType
from ..enum_types import NoticeType
from ..chat import Channel
from ..chat import Tag
import string

class NoticeEvent(Event):

    def __init__(self, notice_type: NoticeType, channel: Channel, tag: Tag, notice_message: string):
        super().__init__(EventType.NOTICE)
        self.__notice_type__ = notice_type
        self.__channel__ = channel
        self.__tag__ = tag
        self.__notice_message__ = notice_message

    def notice_type(self):
        return self.__notice_type__
    
    def channel(self):
        return self.__channel__

    def tag(self):
        return self.__tag__
    
    def notice_message(self):
        return self.__notice_message__