class Tag(object):

    __properties__ = None
    __input__ = None

    def __init__(self, text):
        self.__text__ = text[1:]
        self.__properties__ = dict()
        self.__process_input__()

    # Process tag input
    def __process_input__(self):
        text_split = self.text().split(';')

        for input in text_split:
            values = input.split('=')
            
            if len(values) > 1: 
                self.__add_property__(values[0], values[1])
            else:
                self.__add_property__(values[0], None)

    # Add a property to the properties dictionary
    def __add_property__(self, key, value):
        self.__properties__[key] = value

    # Tag text
    def text(self):
        return self.__text__

    def get(self, key):
        try:
            return self.__properties__[key]
        except KeyError:
            print(f'Could not find {key}')
        return "null"

    def properties(self) -> dict:
        return self.__properties__

    def length(self) -> int:
        return len(self.__properties__)