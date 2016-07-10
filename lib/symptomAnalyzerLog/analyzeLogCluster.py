import sys
import os
import MySQLdb
import re

sys.path.append('.')

from lib.symptom import Symptom
from lib.dbConn import getQueryUnified
from lib.kb.kbLog import KBLog



class LogCluster:
    def __init__(self):
        self.symptoms = self.loadRawSymptoms()
        self.kl = KBLog()
       

    def loadRawSymptoms(self) :
        sql = 'select kbnumber from symptom_log group by kbnumber'
        query = getQueryUnified()
        query.Query(sql)
        

        s = []
        i = 0
        for row in query.record:
            i = i + 1
            print ' %d  loading symptom %d ...' % (i, row['kbnumber'])
            t = Symptom(row['kbnumber'])
            #print t.getLogs()
            s.append(t)
        return s

    def saveCluster(self, s, log, cn):
        sql = 'INSERT INTO `symptom_log_cluster`(`kbnumber`, `log`, `cluster`, `score`) VALUES (%d, "%s", %d, %2.8f)' % (s.getKbnumber(), MySQLdb.escape_string(log['log']), cn, log['score'])
        print sql
        query = getQueryUnified()
        query.Query(sql)

    def analyzeCluster(self, s):
        #all the log clip in symptom
        print s.getLogs()
        for log in s.getLogs():
            #cn is the cluster number
            cn = -1
            cf = True
            for c in self.kl.getLogCluster(s.getKbnumber()):
                cn = cn + 1
                print log['log']
                lr = re.compile(log['log'])
                #if this log clip is found in cluster
                if lr.search(c):
                    self.saveCluster(s, log, cn)
                    cf = False
            if cf:
                #if this log does not belongs to any cluster, just put it to -1 cluster
                self.saveCluster(s, log, -1)


    def process(self):
        print 'start processing log cluster'
        loop = 0
        for s in self.symptoms:
            loop = loop + 1
            print '%d   processing... %d' % (loop, s.getKbnumber())
            self.analyzeCluster(s)
            
        


if __name__ == '__main__':
    lc = LogCluster()
    lc.process()
  
