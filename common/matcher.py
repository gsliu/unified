import sys
import os
import mysql.connector
import MySQLdb
#from .. import symptom

from  symptom import Symptom



class Matcher:
    def __init__(self, minscore=1.0 ):
        self.symptoms = self.loadSymptoms(minscore )
       

    def loadSymptoms(self, minscore) :
        cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        #sql = 'SELECT kbnumber FROM `symptom` where symptomscore > %2.8f ' % minscore
        sql = 'select kbnumber from log_symptom2 group by kbnumber having sum(score) > %2.8f' % minscore
        #sql = u'SELECT * FROM symptom'
        #print sql
        cursor.execute(sql)
        data = cursor.fetchall()
        

        s = []
        i = 0
        for kbnumber in data:
            i = i + 1
            print ' %d  loading symptom %d ...' % (i, kbnumber[0])
            t = Symptom(kbnumber[0])
            #print t.getLogs()
            s.append(t)
        return s

    def getSymptoms(self):
        return self.symptoms


if __name__ == '__main__':
    m = Matcher()
    sym = m.getSymptoms()
    for s in sym:
        print s.getLogs()
   
