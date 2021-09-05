from ..events.event import Event
from ..types.event_type import EventType
from ..types.notice_type import NoticeType
from ..chat.channel import Channel
from ..chat.tag import Tag
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