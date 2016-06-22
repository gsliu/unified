import sys
import re
from esSearchBZLogClip import ESSearchBZLogClip 
sys.path.append("..")
print sys.path

from common.symptom import Symptom 
from symptomAnalyzerLog.mysqlLogClip import MysqlLogClip 

reload(sys);
sys.setdefaultencoding("utf8")



class PRTraining():
    def __init__(self):
        self.es = ESSearchBZLogClip()
        self.logdbs = []

    def addLogTable(self, table):
        self.logdbs.append(MysqlLogClip(table))

    def parseResult(self, esraw, log, logdb):
        #drop this logclip if too many matches
        bzs = []
        if 'hits' in esraw:
            total = int(esraw['hits']['total'])
              
            #update score of lop clip
            if total > 0:
                log['score'] = 0.3 / total
            else:
                log['score'] = 0.0
            #logdb.updateScore(log)

            #10 hits mean this log clip is too common
            if total > 10:
                return bzs
 
            for hit in esraw['hits']['hits']:
                bzs.append(int(hit['_id']))
        return bzs

     
    def process(self):
        for logdb in self.logdbs:
            count = 1
            while logdb.hasNext():
                log = logdb.getNext()
                esraw = self.es.search(log['log'])
            
                count = count + 1
                print("%s: %d =======>%s") % (logdb.getTable(), count, log['log'])
            
                result = self.parseResult(esraw, log, logdb)

                for kbnumber in result:
                    print("   updating sym %d") % kbnumber
                    sym = Symptom(kbnumber)
                    if not sym.hasLog(log):
            #           sym.addLog(log)
                        print "insert log"
                    else:
                        print "updateing log"
             #           sym.updateIncreaseLog(log)

if __name__ == '__main__':
    builder = PRTraining()
    #builder.addLogTable('logclip_view')
    builder.addLogTable('logclip')
    builder.process()
