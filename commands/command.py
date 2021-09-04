import string
from enum_types.source_type import SourceType
from abc import ABC, abstractmethod 

class Command(ABC):
    
    def __init__(self, names):
        self.__source__ = SourceType.TWITCH
        
        if isinstance(names, list):
            self.__names__ = names
        elif isinstance(names, str):
            self.__names__ = [names]

    def names(self):
        return self.__names__
    
    def source(self) -> SourceType:
        return self.__source__

    def set_source(self, source: SourceType):
        self.__source__ = source
    
    @abstractmethod
    async def on_trigger(self, command_event):
        pass