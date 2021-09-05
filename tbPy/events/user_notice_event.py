from ..events import Event
from ..types import EventType
from ..types import UserNoticeType
from ..chat import Channel
from ..chat import Tag
from ..chat import User
import string

class UserNoticeEvent(Event):

    def __init__(self, user_notice_type: UserNoticeType, sender: User, channel: Channel, tag: Tag, notice_message: string):
        super().__init__(EventType.USERNOTICE)
        self.__user_notice_type__ = user_notice_type
        self.__sender__ = sender
        self.__channel__ = channel
        self.__tag__ = tag
        self.__notice_message__ = notice_message
    
    def user_notice_type(self):
        return self.__user_notice_type__

    def sender(self):
        return self.__sender__

    def channel(self):
        return self.__channel__

    def tag(self):
        return self.__tag__

    def notice_message(self):
        return self.__notice_messahe__