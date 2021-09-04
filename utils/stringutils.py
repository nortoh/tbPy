class StringUtils(object):

    # asnyc concat string from array
    async def concat_at(self, start, end, data):
        result = ''
        while start < end:
            result += str(data[start]) + " "
            start += 1
        return result