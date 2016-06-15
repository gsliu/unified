import sys
import re
from esSearchLogClip import ESSearchLogClip 
from mysqlLogClip import MysqlLogClip 
from symptom import Symptom 
from logCheckKBHtml import LogHTMLChecker

class Builder():
    def __init__(self):
        self.es = ESSearchLogClip()
        self.logdb = MysqlLogClip()
        self.lc = LogHTMLChecker()

    def parseResult(self, esraw, log):
        #drop this logclip if too many matches
        kbs = []
        if 'hits' in esraw:
            total = int(esraw['hits']['total'])
              
            #update score of lop clip
            if total > 0:
                log['score'] = 1.0 / total
            else:
                log['score'] = 0.0
            self.logdb.updateScore(log)

            #20 hits mean this log clip is too common
            if total > 20:
                return kbs
 
            for hit in esraw['hits']['hits']:
                kbs.append(int(hit['_id']))
        return kbs

     
    def process(self):
        count = 1
        while self.logdb.hasNext():
            log = self.logdb.getNext()
            esraw = self.es.search(log['log'])
            
            count = count + 1
            print("Log %d =======>%s") % (count, log['log'])
            
            result = self.parseResult(esraw, log)

            for kbnumber in result:
                 if self.lc.check(kbnumber, log['log']):
                     print("   updating sym %d") % kbnumber
                     sym = Symptom(kbnumber)
                     sym.addLog(log)

if __name__ == '__main__':
    builder = Builder()
    builder.process()
