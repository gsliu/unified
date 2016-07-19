import sys
import os
import MySQLdb
import re

sys.path.append('.')

from lib.symptom import Symptom
from lib.dbConn import getQueryUnified
from lib.kb import KB



class BuildSymptom:
    def __init__(self):
        self.symptoms = self.loadRawSymptoms()
       

    def loadRawSymptoms(self) :
        sql = 'select DISTINCT kbnumber from symptom_log'
        query = getQueryUnified()
        query.Query(sql)
        

        s = []
        i = 0
        for row in query.record:
            i = i + 1
            print ' %d  loading symptom %s ...' % (i, row['kbnumber'])
            t = Symptom(row['kbnumber'])
            #print t.getLogs()
            s.append(t)
        return s

    def analyzeCluster(self, s):
        #all the log clip in symptom
        #print s.getLogs()
        for log in s.getLogs():
            #cn is the cluster number
            cn = -1
            cf = True
            kb = KB(s.getKbnumber())
            for c in kb.getLogCluster():
                cn = cn + 1
                #print log['log']
                c = c.lower()
                lr = re.compile(re.escape(log['log']))
                #if this log clip is found in cluster
                if lr.search(c):
                    s.saveCluster(log, cn)
                    cf = False
            if cf:
                #if this log does not belongs to any cluster, just put it to -1 cluster
                s.saveCluster(log, -1)


    def process(self):
        print 'start processing log cluster'
        loop = 0
        for s in self.symptoms:
            loop = loop + 1
            print '%d   processing... %s' % (loop, s.getKbnumber())
            self.analyzeCluster(s)
            
        


if __name__ == '__main__':
    lc = BuildSymptom()
    lc.process()
  
