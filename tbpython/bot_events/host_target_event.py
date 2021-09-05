from ..enum_types.event_type import EventType
from ..bot_events.event import Event
from ..chat.user import User
from ..chat.channel import Channel

class HostTargetEvent(Event):

    def __init__(self, host_channel: Channel, hosted_channel: Channel, amount: int):
        super().__init__(EventType.HOSTTARGET)
        self.__host_channel__ = host_channel
        self.__hosted_channel__ = hosted_channel
        self.__amount__ = amount

    def host_channel(self):
        return self.__host_channel__

    def hosted_channel(self):
        return self.__hosted_channel__
    
    def amount(self):
        return self.__amount__