import re

class FullText:
    def __init__(self, seperator=r'[^A-Za-z0-9\-\_\.\,]'):
        self.seperator = seperator
        #[{'name':name, 'line':1, 'offset':1}]
        self.indexData = {}
         
    def index(self, name, text):
        text = text.encode('utf-8', 'ignore')
        text = text.lower()
        lineNumber = 0
        lines = text.split('\n')
        #print lines
        for line in lines:
            offset = 0
            tokens = re.split(self.seperator, line)
            tokens = filter(None, tokens) 
            for token in tokens:
                #print# token
                ind = {'name':name, 'line':lineNumber, 'offset':offset}
                if self.indexData.has_key(token):
                    self.indexData[token].append(ind)
                else:
                    self.indexData[token] = [ind]
                offset = offset + 1
            lineNumber = lineNumber + 1

    def searchToken(self, token):
        if self.indexData.has_key(token):
            return self.indexData[token]
        return []

    def search(self, query):
        ret = []
        queryTokens = re.split(self.seperator, query)
        queryTokens = filter(None, queryTokens) 

        if len(queryTokens) == 0:
            return ret
        else:
            ret = self.searchToken(queryTokens[0])

        for token in queryTokens[1:]:
            if self.indexData.has_key(token):
                nret = self.indexData[token]
                mret = []
                for r in ret:
                    for n in nret:
                        if r['name'] == n['name'] and r['line'] == n['line'] and (r['offset'] + 1) == n['offset']:
                            mret.append(n)
                ret = mret
                    
            else:
                return []
        return ret
        





if __name__ == '__main__':
    ft = FullText()
    #ft.index('text', 'abc')
    ft.index('text', 'abc_bc\n bcd\n os x 10.10 abc bcd\n ccd:::ef\n os x, 10.10 tesafdalkjlj\n fangchi, shiyao, bead\n')
    text = 'abc_bc\n bcd\n os x 10.10 abc bcd\n ccd:::ef\n os x, 10.10 tesafdalkjlj\n fangchi, shiyao, bead\n'
    print ft.indexData
    print ft.search('abc_bc ::')
    print ft.search('ccd ef')
    i = 0
    while i < 16000000:
       i = i + 1
       ft.search('shiyao bead')
       #'shiyao bead' in text
    print 'done'
