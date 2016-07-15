import re

from HTMLParser import HTMLParser
import sys

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d): self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class KBLog:
    def __init__(self, kbdir='/data/kbdata'):
        self.regs = []
        self.regs.append(re.compile(r'(<font[^>]+?courier new*.+?<\/font>)'))
        self.regs.append(re.compile(r'(<span[^>].+?courier new*.+?<\/span>)'))
        self.regs.append(re.compile(r'(<li[^>]+?courier new*.+?<\/li>)'))
        self.regs.append(re.compile(r'(<code*.+?<\/code>)'))
        self.regs.append(re.compile(r'(<tt*.+?<\/tt>)'))
        self.kbdir = kbdir

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()


    def readfile(self, kbnumber):
        f = open(self.kbdir + '/' +  str(kbnumber))
        return f.read().lower()
        
    def getLog(self, kbnumber):
        kblog = ""
        text = self.readfile(kbnumber)
        #print text
        for reg in self.regs:
            m1 = reg.findall(text)
            #print reg 
            if m1:
                for string in m1:
                    kblog = kblog + self.strip_tags(string)
        return kblog
    def getLogCluster(self, kbnumber):
        cluster = []
        n = 0
        text = self.readfile(kbnumber)
        for reg in self.regs:
            m1 = reg.findall(text)
            if m1:
                for string in m1:
                    #kblog = kblog + self.strip_tags(string)
                    cluster.append(self.strip_tags(string))
        return cluster

        
        
    def check(self, kbnumber, log):
        
        try:
            if log in self.getLog(kbnumber):
                return True
        except:
            return False
        return False

if __name__ == '__main__':
    lc = KBLog()
    #print lc.check(1037071, 'A general system error occured')
    #print lc.check(1037071, ' B A general system error occured')
    #print lc.check(1030267, 'A general system error occured')
    #print lc.getLog(1002799)
    #print lc.getLogCluster(1002799)
    #print lc.getLogCluster(1000959)
    #print lc.getLogCluster(1000082)
    #print lc.getLogCluster(1003484)
    #print lc.getLogCluster(1014508)
    print lc.getLogCluster(1003979)
    #print lc.getLog(1001101)
    #print lc.getLogCluster(1189)
    #print lc.getLog(1037071) 
    #print lc.getLog(1030267) 
    #print lc.getLogCluster(2057902) 
        
        
