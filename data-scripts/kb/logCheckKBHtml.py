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
        self.regs = []
        self.regs.append(re.compile(r'(<font[^>]+?Courier New*.+?<\/font>)'))
        self.regs.append(re.compile(r'(<span[^>].+?Courier New*.+?<\/span>)'))
        self.regs.append(re.compile(r'(<li[^>]+?Courier New*.+?<\/li>)'))
        self.regs.append(re.compile(r'(<code*.+?<\/code>)'))
        self.kbdir = kbdir

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()


    def readfile(self, kbnumber):
        f = open(self.kbdir + '/' +  str(kbnumber))
        return f.read()
        
    def getLog(self, kbnumber):
        kblog = ""
        text = self.readfile(kbnumber)
        for reg in self.regs:
            m1 = reg.findall(text)
            if m1:
                for string in m1:
                    kblog = kblog + self.strip_tags(string)
        return kblog
    def check(self, kbnumber, log):
        
        try:
            if log in self.getLog(kbnumber):
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
    #print lc.getLog(1037071) 
    #print lc.getLog(1030267) 
    print lc.getLog(2057902) 
        
        
