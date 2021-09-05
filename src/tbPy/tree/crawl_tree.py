

"""

We want to parse data that is dependent on two factors: channel_crawled, channel_crawled_from

We we want to add a new channel that was crawled to the tree, we must first look for the index

"""
class CrawlTree(object):

    def __init__(self):
        self.index_map = dict()
        self.root = None

    def create_node(self, key):
        return CrawlNode(key)

    def append_key(self, key):

        # If root is null
        if self.root is None:
            pass
        else:
            pass

class CrawlNode(object):

    def __init__(self, key):
        self.key = key
        self.child = []