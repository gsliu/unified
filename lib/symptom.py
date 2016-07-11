import re
import random
import MySQLdb

from dbConn import getQueryUnified




class Symptom:
    def __init__(self, kb):

        #sql = 'SELECT * FROM `symptom` where kbnumber = ' +  str(kb)
        #query = getQueryUnified()
        #query.Query(sql)
        #data = query.record


        self.kbnumber = kb
        self.logs = []
        self.keywords = []
        self.loadLog()
        self.loadKeyword()
        #if data:
        #    self.new = 0
        #    self.loadLog()
        #    self.loadKeyword()
        #else:
        #    self.new = 1
        #    self.logcount = 0
        #    self.symptomscore = 0
    
    def loadLog(self):
        sql = 'SELECT * FROM `symptom_log` where kbnumber = "%s"' % self.kbnumber
        query = getQueryUnified()
        query.Query(sql)
        data = query.record


        for row in data:
          # print row
           self.logs.append({'log':row['log'], 'score':float(row['score'])})

    def loadKeyword(self):
        sql = 'SELECT * FROM `symptom_keyword` where kbnumber = "%s"' % self.kbnumber
        query = getQueryUnified()
        query.Query(sql)
        data = query.record
        for row in data:
           self.keywords.append({'keyword':row['keyword'], 'score':float(row['score'])})



     
    def addLog(self, log):
        #print log
        sql = 'INSERT INTO `symptom_log` (`kbnumber`, `log`, `score` ) VALUES ("%s", "%s" , %2.8f)' % ( self.kbnumber, MySQLdb.escape_string(log['log']), log['score'])
        print sql
        query = getQueryUnified()
        query.Query(sql)

    def getKbnumber(self):
        return self.kbnumber

    def getScore(self):
        return self.score
 
    def getKeywords(self):
        return self.keywords


 
    def getLogs(self):
        return self.logs

    def getKeywordsDemo(self):
        ret = 'name,count\n'
        loop = 0 
        for keyword in self.getKeywords():
            loop = loop + 1
            if loop > 50:
                break
            #if log['score'] < 0.21:
            #    continue
         
            ret = ret + keyword['keyword'] + ',' + str(keyword['score'] * random.randint(1, 10) + 1) + '\n'
        return ret


    def getLogsDemo(self):
        ret = 'name,count\n'
        loop = 0 
        for log in self.getLogs():
            loop = loop + 1
            if loop > 50:
                break
            #if log['score'] < 0.21:
            #    continue
            l = re.sub('[^a-zA-Z _:-]', "", log['log'])
            l = l.strip()
            words = l.split(' ')
            lc = ""
            
            for w in words:
                lc = lc + w + ' '
                if len(lc) > 15:
                    break

                 
            lc.strip()
            if len(lc) > 20:
                lc = lc[0:16] + '...'
         
            ret = ret + lc + ',' + str(log['score'] *100) + '\n'

        return ret
    def hasLog(self,log):
        for l in self.logs:
            if log['log'] == l['log']:
                return True
        return False

    def updateIncreaseLog(self, log):
        for l in self.logs:
            if l['log'] == log['log']:
                l['score'] = l['score'] + log['score']
                self.updateLog(l)

    def updateDecreaseLog(self, log):
        for l in self.logs:
            if l['log'] == log['log']:
                l['score'] = l['score'] - log['score']
                self.updateLog(l)

    #mark a log as scan when it's scaned
    def markLog(self, log):
        sql = 'UPDATE `symptom_log` SET `scan`= 1 WHERE kbnumber = "%s" and log = "%s"' % ( self.getKbnumber(), log['log'])
        query = getQueryUnified()
        query.Query(sql)

    def saveCluster(self, log, cn): 
        sql = 'INSERT INTO `symptom_log_cluster`(`kbnumber`, `log`, `cluster`, `score`) VALUES ("%s", "%s", %d, %2.8f)' % (self.getKbnumber(), MySQLdb.escape_string(log['log']), cn, log['score']) 
        print sql 
        query = getQueryUnified() 
        query.Query(sql) 

    def loadCluster(self):
        sql = 'SELECT log, score, cluster FROM `symptom_log_cluster` WHERE kbnumber = "%s"' %  self.kbnumber
        query = getQueryUnified()
        query.Query(sql)
        data = query.record
        print data





if __name__ == "__main__":
    s = Symptom("1017910")
    s = Symptom("2035011")
    s = Symptom("219")

    #log1 = {'log':'test log', 'score':float(0.123)}
    #s.addLog(log1)
    #print s.getLogs()
    #log2 = {'log':'test log2', 'score':float(1.523)}
    #s.addLog(log2)
    #print s.getLogs()
        
    #log = {}
    #log['log'] = 'ToolsBackup: '
    #log['score'] = 0.3
    #print s.hasLog(log)
    #s.updateIncreaseLog(log)
    print s.getLogs()
    print s.getKeywords()
    print s.getKeywordsDemo()
    print s.loadCluster()
