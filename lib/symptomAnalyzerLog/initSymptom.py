import sys
import re
sys.path.append(".")

from lib.symptom import Symptom 
from lib.logClip.esSearchLogClip import ESSearchLogClip 
from lib.logClip.mysqlLogClip import MysqlLogClip 

reload(sys);
sys.setdefaultencoding("utf8")



class InitSymptom():
    def __init__(self):
        self.es = ESSearchLogClip()
        self.logdbs = []

    def addLogTable(self, table):
        self.logdbs.append(MysqlLogClip(table))

    def parseResult(self, esraw, log, logdb):
        #drop this logclip if too many matches
        kbs = []
        if 'hits' in esraw:
            total = int(esraw['hits']['total'])
              
            #update score of lop clip
            if total > 0:
                log['score'] = 1.0 / total
            else:
                log['score'] = 0.0

            #20 hits mean this log clip is too common
            if total > 20:
                return kbs
 
            for hit in esraw['hits']['hits']:
                kbs.append(int(hit['_id']))
        return kbs

     
    def process(self):
        for logdb in self.logdbs:
            count = 1
            while logdb.hasNext():
                #fetech next log
                log = logdb.getNext()
                #mark this log as scaned
                logdb.updateScan(log)
                
                #search this log in es
                esraw = self.es.search(log['log'])
                count = count + 1
                print("%s: %d =======>%s") % (logdb.getTable(), count, log['log'])
            
                result = self.parseResult(esraw, log, logdb)

                for kbnumber in result:
                    print("   updating sym %s") % str(kbnumber)
                    sym = Symptom(str(kbnumber))
                    if sym.hasLog(log):
                        #sym.updateIncreaseLog(log)
                        continue
                    else:
                        sym.addLog(log)

if __name__ == '__main__':
    builder = InitSymptom()
    #builder.addLogTable('logclip_view')
    builder.addLogTable('logclip')
    builder.process()
