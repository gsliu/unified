
class LineDict:
    def __init__(self, text):
        self.textLine = self.textToDictLine(text)


    def getLines(self, query):
        if self.textLine.has_key(query):
            return self.textLine[query]
        return None

    def textToDictLine(self, text):
        textLine = {}
        i = 0
        for line in  text.split('\n'):
            for token in line.split():
                if textLine.has_key(token):
                    textLine[token].append(i)
                else:
                    textLine[token] = [i]
            i = i + 1
        return textLine




if __name__ == '__main__':
    ld = LineDict('abc bcd ab*12 a_ad:\n a^a\n abc\n b\n :::')
    print ld.getLines('abc')
    print ld.getLines('b')
    print ld.getLines(':::')
    print ld.getLines('a_ad:')
