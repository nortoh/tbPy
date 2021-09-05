from . import User

class Channel(object):

    def __init__(self, name):
        self.__name__ = name
        self.__users__ = dict()
        
    def add_user(self, user: User):
        if user not in self.__users__:
            self.__users__[user.name()] = user

    def remove_user(self, user: User):
        if user in self.__users__:
            del self.__users__[user.name()]

    def get_user(self, name) -> User:
        if name in self.__users__:
            return self.__users__[name]

    def has_user(self, name):
        if self.get_user(name) != None: return True
        return False
    
    def get_users(self) -> dict:
        return self.__users__

    def tag(self):
        return self.tag

    def name(self) -> str:
        return self.__name__.lower()

    def id(self):
        if self.tag is None:
            return 0
        return self.tag.get('room-id')