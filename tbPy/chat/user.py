class User(object):

    # User constructor
    def __init__(self, name):
        self.__name__ = name
    
    # Retrives the badges of the user
    def get_badges(self) -> dict():
        # Create an empty dictionary
        badge_dictionary = dict()

        # Gets the badges string from the tag
        badge_str = self.tag.get('badges')

        # If tag is not set, or contains no badges, send an empty dict
        if self.tag is None or self.tag.length() == 0:
            return badge_dictionary
        
        # Split the different badges
        badges = badge_str.split(',')

        # For each seperate badge in badges
        for badge in badges:
            # Seperate badge name and version
            badge_vals = badge.split('/')

            # Skip predictions until implemented
            # TODO: Predictions
            if badge_vals[0] != 'predictions':
                badge_dictionary[badge_vals[0]] = int(badge_vals[1])
        
        return badge_dictionary

    # If user has badge
    def has_badge(self, badge) -> bool:
        if badge in self.get_badges(): return True
        return False

    # If user has badge and version
    def has_badge_version(self, badge, version) -> bool:
        if badge in self.get_badges():
            ver = self.get_badges()[badge]
            return version == ver
        return False

    # If user is a subscriber
    def is_subscriber(self) -> bool:
        return self.has_badge('subscriber')

    # If user is a moderator
    def is_moderator(self) -> bool:
        return self.has_badge('moderator')
    
    # If user is the broadcaster
    def is_broadcaster(self) -> bool:
        return self.has_badge('broadcaster')

    # If user is a VIP
    def is_vip(self) -> bool:
        return self.has_badge('vip')

    # Username
    def name(self) -> str:
        return self.__name__.lower()