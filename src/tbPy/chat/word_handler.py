class WordHandler(object):

    def __init__(self):
        self.channel_word_count = dict()

    def handle_message(self, message):
        channel_name = message.channel().name()
        words = message.text().strip().lower().split(' ')
        words_len = len(words)

        # Channel has a count already
        if channel_name in self.channel_word_count:
            curr = int(self.channel_word_count[channel_name])
            curr += words_len
            self.channel_word_count[channel_name] = curr

        # Channel does not have a count
        else:
            self.channel_word_count[channel_name] = words_len