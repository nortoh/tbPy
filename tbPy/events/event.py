from ..types.event_type import EventType

class Event(object):

    def __init__(self, type: EventType):
        self.__type = type
        
    def type(self):
        return self.__type