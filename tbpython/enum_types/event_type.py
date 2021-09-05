from enum import Enum

class EventType(Enum):
        STARTUP = 1
        SHUTDOWN = 2
        TICK = 3
        PING = 4
        COMMAND = 5
        MESSAGE = 6
        JOIN = 7
        PART = 8
        NOTICE = 9
        CLEARCHAT = 10
        CLEARMSG = 11
        ROOMSTATE = 12
        USERSTATE = 13
        USERNOTICE = 14
        HOSTTARGET = 15
        CONNECTED = 16
        CUSTOM = 17
        WHISPER = 18
        CUSTOMWORDTRIGGER = 19
        WORDTRIGGER = 20
        DEBUGLINE = 21
        EXCEPTION = 22
        RECONNECT = 23
        NEWDAY = 24
        BITCHEER = 25
        MENTION = 26
        ERROR = 27
        DISCONNECTED = 28