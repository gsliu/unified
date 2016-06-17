import re
import MySQLdb
import mysql.connector
import MySQLdb.cursors

class Symptom:
    def __init__(self, kb):

        global cnx
        cnx = mysql.connector.connect(user='root',password='vmware', database='unified')

        global cursor
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
	sql = 'SELECT * FROM `symptom` where kbnumber = ' +  str(kb)
        cursor.execute(sql)
        self.data = cursor.fetchall()

        #print self.data
        self.kbnumber = kb
        self.logs = []
        if self.data:
            self.symptomscore = self.data[0][3]
            self.logcount = self.data[0][4]
            self.new = 0
            self.loadLog()
        else:
            self.new = 1
            self.logcount = 0
            self.symptomscore = 0
    
    def loadLog(self):
        sql = 'SELECT * FROM `log_symptom` where kbnumber = ' +  str(self.kbnumber)
        cursor.execute(sql)
        self.data = cursor.fetchall()
        for row in self.data:
          # print row
           self.logs.append({'log':row[1], 'score':float(row[2])})

     
    def addLog(self, log):
        self.logcount = self.logcount + 1
        self.symptomscore = self.symptomscore + log['score']  
        #print log
        sql = 'INSERT INTO `log_symptom`(`kbnumber`, `log`, `score` ) VALUES (%d, "%s" , %2.8f)' % ( self.kbnumber, log['log'], log['score'])
        print sql
        cursor.execute(sql)
        cnx.commit()
        self.save()

    def getKbnumber(self):
        return self.kbnumber

    def getScore(self):
        return self.score
 
    def getLogs(self):
        return self.logs

    def deleteLog(self, log):
   
        sql = 'delete from log_symptom where kbnumber = %d and log = "%s"' % ( self.kbnumber, log['log'])
        cursor.execute(sql)
        cnx.commit()
        self.save()
        self.logcount = self.logcount - 1
        self.symptomscore = self.symptomscore - log['score']  

        self.logcount = len(logs)
        self.save()

    def save(self):
        if self.new == 1:
            sql = 'INSERT INTO `symptom`(`kbnumber`, `symptomscore`, `logcount` ) VALUES (%d, %2.8f , %d)' % ( self.kbnumber, self.symptomscore, self.logcount)
        else:
            sql = 'UPDATE symptom SET `kbnumber`= "%d",`symptomscore`=%2.8f, `logcount` = %d WHERE `kbnumber`=%d ' % (self.kbnumber, self.symptomscore, self.logcount, self.kbnumber)
            
        #print sql
        cursor.execute(sql)
        cnx.commit()




if __name__ == "__main__":
    s = Symptom(1009484)
    log1 = {'log':'test log', 'score':float(0.123)}
    s.addLog(log1)
    print s.getLogs()
    log2 = {'log':'test log2', 'score':float(1.523)}
    s.addLog(log2)
    print s.getLogs()
        
