import sys
import re
import mysql
import MySQLdb
from esSearchBZLogClip import ESSearchBZLogClip 
sys.path.append("..")
print sys.path

from dataScripts.bz.db_bz import get_bz_con

from common.symptom import Symptom 
from symptomAnalyzerLog.mysqlLogClip import MysqlLogClip 

reload(sys);
sys.setdefaultencoding("utf8")



class PRTraining():
    def __init__(self):
        self.es = ESSearchBZLogClip()
        self.logdbs = []
        self.bz_con, self.bz_cur = get_bz_con()

   
        pr_kb_sql = 'select bug_id, kb_id from bug_kb_map'
        self.bz_cur.execute(pr_kb_sql)
        data = self.bz_cur.fetchall()
        self.pr_kb = {}
        for d in data:
            print d
            if not self.pr_kb.has_key(str(d[0])):
                self.pr_kb[str(d[0])] = []
            self.pr_kb[str(d[0])].append(d[1])



        self.sdict = {}
        sqlkb = 'select kbnumber from symptom'
        cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sqlkb)
        data = cursor.fetchall()
        for d in data:
            self.sdict[str(d[0])] = 1


    def addLogTable(self, table):
        self.logdbs.append(MysqlLogClip(table))

    def parseResult(self, esraw, log, logdb):
        #drop this logclip if too many matches
        kbs = []
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
                return kbs 
 
            for hit in esraw['hits']['hits']:
               
                if self.pr_kb.has_key(str(hit['_id'])):
                    for kb in self.pr_kb[str(hit['_id'])]:
                        if self.sdict.has_key(kb):
                            kbs.append(kb)
                            print 'found kb %s, bug %s' % (kb, str(hit['_id']))
                    
        return kbs

     
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
                    print("   updating sym %s") % kbnumber
                    sym = Symptom(int(kbnumber))
                    if not sym.hasLog(log):
                        sym.addLog(log)
                        print "insert log"
                    else:
                        print "updateing log"
                        sym.updateIncreaseLog(log)
#
if __name__ == '__main__':
    builder = PRTraining()
    #builder.addLogTable('logclip_view')
    builder.addLogTable('logclip')
    builder.process()
