from os import listdir
from os.path import isfile, join
import sys
sys.path.append('.')

from lib.kb import KB
from lib.logClip.analyzeText import AnalyzeText

class ScanKBLog:
    def __init__(self, kbDir='/data/kb/data'):
        self.kbDir = kbDir
        self.ta = AnalyzeText()
   
    def processKBLog(self, page):
        #to lower
        kblog = page.getFullText().lower()
        if len(kblog) > 0:
            self.ta.analyze(kblog)

    def process(self):
        # iter all kbs
        for f in listdir(self.kbDir):
            print "DEBUG: %s" %(f)
            file = join(self.kbDir, f)
            if isfile(file):
                self.processKBLog(KB(file))

if __name__ == "__main__":
   loader = ScanKBLog('/data/kbdata')
   loader.process()
