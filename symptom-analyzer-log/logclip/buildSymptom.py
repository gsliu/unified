import sys
import re
from esSearchLogClip import ESSearchLogClip 
from mysqlLoadLogClip import MysqlLoadLogClip 
from symptom import Symptom 
from logCheckKBHtml import LogHTMLChecker

class Builder():
    def __init__(self):
        self.es = ESSearchLogClip()
        self.mysql = MysqlLoadLogClip()
        self.lc = LogHTMLChecker()
     
    def process(self):
        while self.mysql.hasNext():
            logclip = self.mysql.getNext()
            print("LOG=======>%s") % logclip
            result = self.es.search(logclip)
            for kbnumber in result:
                 if self.lc.check(kbnumber, logclip):
                     print("   updating sym %d") % kbnumber
                     sym = Symptom(kbnumber)
                     sym.addLog(logclip)

if __name__ == '__main__':
    builder = Builder()
    builder.process()
