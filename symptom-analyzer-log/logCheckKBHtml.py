import re

from HTMLParser import HTMLParser
import sys

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class LogHTMLChecker:
    def __init__(self, kbdir='/data/data/kbraw/data'):
        self.reg1 = re.compile(r'(<font*.+Courier New*.+<\/font>)')
        self.reg2 = re.compile(r'(<span*.+Courier New*.+<\/span>)')
        self.reg3 = re.compile(r'(<li*.+Courier New*.+<\/li>)')
        self.reg4 = re.compile(r'(<code*.+Courier New*.+<\/code>)')
        self.kbdir = kbdir

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()


    def readfile(self, kbnumber):
        f = open(self.kbdir + '/' +  str(kbnumber))
        return f.read()
        
    def check(self, kbnumber, log):
        kblog = ""
        text = self.readfile(kbnumber)
        m1 = self.reg1.findall(text)
        if m1:
            for string in m1:
                kblog = kblog + self.strip_tags(string)

            
        m2 = self.reg2.findall(text)
        if m2:
            for string in m2:
                kblog = kblog + self.strip_tags(string)
            


        m3 = self.reg3.findall(text)
        if m3:
            for string in m3:
                kblog = kblog + self.strip_tags(string)


        m4 = self.reg4.findall(text)
        if m4:
            for string in m4:
                kblog = kblog + self.strip_tags(string)

        #print kblog
        try:
            if log in kblog:
                return True
        except:
            return False
        return False

if __name__ == '__main__':
    lc = LogHTMLChecker('/data/data/kbraw/data')
    print lc.check(1037071, 'A general system error occured')
    print lc.check(1037071, ' B A general system error occured')
    print lc.check(1030267, 'A general system error occured')
    print lc.check(1030267, 'write function failed')
    
    print sys.getdefaultencoding()
        
        
