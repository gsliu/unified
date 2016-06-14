import re
import MySQLdb
import mysql.connector
import MySQLdb.cursors

class Symptom:
    def __init__(self, kb):

        self.cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        #self.cursor = self.cnx.cursor()
        self.cursor = self.cnx.cursor(MySQLdb.cursors.DictCursor)
	sql = 'SELECT * FROM `log_kb_raw` where kbnumber = ' +  str(kb)
        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()

        self.kbnumber = kb
        if self.data:
            self.new = 0
            self.loadKB()
        else:
            self.new = 1
            self.lognumber = 0

    
    def loadKB(self):
        self.fulllog = self.data[0][1]
        self.lognumber = self.data[0][2]
     
    def addLog(self, log):
        self.lognumber = self.lognumber + 1
        if self.lognumber == 1:
            self.fulllog = log
        else:
            self.fulllog = self.fulllog + '#$#$' + log
        self.save()

    def getFullLog(self):
        return self.fulllog

    def getLogs(self):
        return self.fulllog.split('#$#$')

    def updateFullLog(self, fulllog):
        self.fulllog = fulllog      
        logs = fulllog.split('#$#$')
        self.lognumber = len(logs)
        self.save()

    def save(self):
        if self.new == 1:
            sql = 'INSERT INTO `log_kb_raw`(`kbnumber`, `logs`, `lognumber`) VALUES (%d, \"%s\", %d)' % ( self.kbnumber, self.fulllog, self.lognumber)
        else:
            sql = 'UPDATE `log_kb_raw` SET `logs`= "%s",`lognumber`=%d WHERE `kbnumber`=%d ' % (self.fulllog, self.lognumber, self.kbnumber)
            
        print sql
        self.cursor.execute(sql)
        self.cnx.commit()




if __name__ == "__main__":
    s = Symptom(1009484)
    s.addLog("test log 3")
    print s.getLogs()
    s.updateFullLog("aaaaa")
    print s.getLogs()
        
