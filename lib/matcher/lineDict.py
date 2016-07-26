class LineDict:
    def __init__(self, text):
        self.textLines = self.textToDictLine(text)


    def getLines(self, query):
        ret = []
        i = 0
        for line in self.textLines:
            if query in line:
                ret.append(i)
                i = i + 1
        if len(ret) == 0:
            return None
        else:
            return ret
           

    def textToDictLine(self, text):
        textLines = text.split('\n')
        return textLines




if __name__ == '__main__':
    ld = LineDict('abc bcd ab*12 a_ad:\n a^a\n abc\n b\n :::')
    print ld.getLines('abc')
    print ld.getLines('b')
    print ld.getLines(':::')
    print ld.getLines('a')
