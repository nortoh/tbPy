from enum import Enum

class IRCType(Enum):
    CAP = 1
    PING = 2
    CTCP = 3
    JOIN = 4
    PART = 5
    PRIVMSG = 6
    CLEARCHAT = 7
    CLEARMSG = 8
    NOTICE = 9
    USERNOTICE = 10
    ROOMSTATE = 11
    USERSTATE = 12
    HOSTTARGET = 13
    WHISPER = 14
    RECONNECT = 15
    UNKNOWN = 16