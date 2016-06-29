import re
import MySQLdb
import mysql.connector
import MySQLdb.cursors
import sys
import json
import datetime
sys.path.append('..')

from dataScripts.kb.webpage import IKBPage


cnx = mysql.connector.connect(user='root',password='vmware', database='unified', buffered=True)

cursor = cnx.cursor(MySQLdb.cursors.DictCursor )
   

class SymptomHits:
    def topHits(self):
        sql = 'select kbnumber,  sum(hits) as total from symptom_hits group by kbnumber ORDER by total DESC'
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor )
        cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
        for row in data:
          # print row
           ret.append({'kbnumber':row[0], 'hits':row[1]})
        ret = ret[0:15]
        cursor.close()
        return ret

    def hit(self, kbnumber):
        #d = datetime.datetime.strptime('my date', "%b %d %Y %H:%M")
        sql = 'INSERT INTO `symptom_hits`(`kbnumber`, `hits`, `time` ) VALUES (%d, 1, CURRENT_DATE())' % ( kbnumber)
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor )
        print sql
        cursor.execute(sql)
        cnx.commit()
        cursor.close()

    def getHits(self, kbnumber):
        sql = 'select sum(hits) from symptom_hits where kbnumber = %d' % kbnumber
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor )
        cursor.execute(sql)
        data = cursor.fetchall()
          # print row
        cursor.close()
        return data[0][0]
  
    def topHitsFull(self):
        kbs = self.topHits()
        jret = []
        
        for kb in kbs:
            try:
                page = IKBPage('/data/data/kbraw/data/%s' % kb['kbnumber'])
                j = dict()
                j['url'] = 'http://kb.vmware.com/kb/%d' % kb['kbnumber']
                j['title'] = page.get_title()
                j['text'] = page.get_text()[0:300] + '...'
                #j['text'] = 'aaaaaa'
                j['hits'] = str(kb['hits']) + ' hits'
        
                jret.append(j)
            except:
                pass
        jret = jret[0:10]
        return jret
        #print j
    def getGroupHits(self, kbnumber):

        cursor = cnx.cursor(MySQLdb.cursors.DictCursor )
        sql = 'SELECT DATE(time) DateOnly,  SUM(hits) FROM symptom_hits where kbnumber = %d GROUP BY DateOnly' % kbnumber
        print sql
        cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
        for d in data:
            h = {'time':d[0].strftime('%d, %b %Y'), 'hits': str(d[1])}
            ret.append(h)
        print ret
        cursor.close()
        return ret
        
 







if __name__ == "__main__":
    s = SymptomHits()
    #s.hit(1009484)
    #s.hit(1031636)
    #s.hit(1005266)   
    #print s.topHits()

    print s.topHitsFull()
    #print json.dumps(s.topHitsFull())
    
    #print s.getGroupHits(2120653)
        
