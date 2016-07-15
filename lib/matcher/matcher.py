import sys
import os
sys.path.append('.')

from lib.symptom import Symptom
from lib.dbConn import getQueryUnified



class Matcher:
    def __init__(self, minscore=0.5 ):
        self.symptoms = self.loadSymptoms(minscore )
       

    def loadSymptoms(self, minscore) :
        sql = 'select kbnumber from symptom_log_cluster group by kbnumber having sum(score) > %2.8f' % minscore
        query = getQueryUnified()
        query.Query(sql)

        print query.record
        
        

        s = []
        i = 0
        for row in query.record:
            i = i + 1
            print ' %d  loading symptom %s ...' % (i, row['kbnumber'])
            t = Symptom(row['kbnumber'])
            #print t.getLogs()
            s.append(t)
        return s

    def getSymptoms(self):
        return self.symptoms

    def findSymptom(self, kbnumber):
        for s in self.symptoms:
            if s.getKbnumber() == kbnumber:
                return s
        return None


if __name__ == '__main__':
    m = Matcher()
    sym = m.getSymptoms()
    #s = m.findSymptom(1010733)
    #print s.getLogs()
    #for s in sym:
    #    print s.getLogs()
   
