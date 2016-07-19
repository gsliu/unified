import re
import sys
import json
import datetime

sys.path.append('.')
from lib.kb import KB
from lib.dbConn import getQueryUnified



   

class SymptomHits:
    def topHits(self):
        sql = 'select kbnumber,  sum(hits) as total from symptom_hits group by kbnumber ORDER by total DESC'
        query = getQueryUnified()
        query.Query(sql)
        data = query.record


        ret = []
        for row in data:
          # print row
           ret.append({'kbnumber':row['kbnumber'], 'hits':row['total']})
        ret = ret[0:15]
        return ret

    def hit(self, kbnumber):
        #d = datetime.datetime.strptime('my date', "%b %d %Y %H:%M")
        sql = 'INSERT INTO `symptom_hits`(`kbnumber`, `hits`, `time` ) VALUES (%d, 1, CURRENT_DATE())' % ( kbnumber)
        query = getQueryUnified()
        query.Query(sql)
        print sql

    def getHits(self, kbnumber):
        sql = 'select sum(hits) as total from symptom_hits where kbnumber = %d' % kbnumber
        query = getQueryUnified()
        query.Query(sql)
        data = query.record
        return data[0]['total']
  
    def topHitsFull(self):
        kbs = self.topHits()
        jret = []
        
        for kb in kbs:
            try:
                page = KB(kb['kbnumber'])
                j = dict()
                j['url'] = page.getUrl()
                j['title'] = page.getTitle()
                j['text'] = page.getText()[0:300] + '...'
                j['hits'] = str(kb['hits']) + ' hits'
        
                jret.append(j)
            except:
                pass
        jret = jret[0:10]
        return jret
        #print j
    def getGroupHits(self, kbnumber):

        sql = 'SELECT DATE(time) DateOnly ,  SUM(hits) as total FROM symptom_hits where kbnumber = %d GROUP BY DateOnly' % kbnumber
        print sql
        query = getQueryUnified()
        query.Query(sql)
        data = query.record


        ret = []
        for d in data:
            h = {'time':d['DateOnly'].strftime('%d, %b %Y'), 'hits': str(d['total'])}
            ret.append(h)
        return ret
        
 







if __name__ == "__main__":
    s = SymptomHits()
    s.hit(1009484)
    s.hit(1031636)
    s.hit(1005266)   
    print s.topHits()

    print s.topHitsFull()
    #print json.dumps(s.topHitsFull())
    
    #print s.getGroupHits(2120653)
        
