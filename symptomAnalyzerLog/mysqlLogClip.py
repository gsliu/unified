import re
import mysql
import mysql.connector
 
ucnx = mysql.connector.connect(user='root',password='vmware', database='unified')
     
class MysqlLogClip:
    def __init__(self, table):
        self.table = table
        self.cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        self.cursor = self.cnx.cursor()
        self.cursor.execute('SELECT log, score FROM %s ' % self.table)
        self.data = self.cursor.fetchall()
	self.i = 0

    def getNext(self):
        if self.i < len(self.data):
            row = self.data[self.i]
            self.i = self.i + 1
            return {'log':row[0], 'score':row[1]}

        return None

    def hasNext(self):
        if self.i < len(self.data):
            return True
        return False
    def getTable(self):
        return self.table
    
    def updateScore(self, log):
 
#        ucnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        ucursor = ucnx.cursor()
 
        sql = ('UPDATE %s SET `score`=%2.8f WHERE log = "%s"') % (self.table, log['score'], log['log'])
        #print sql
        ucursor.execute(sql)
        ucnx.commit()
#        ucursor.close()
#        ucnx.close()



if __name__ == '__main__':
    loader = MysqlLogClip('logclip_view')
    while loader.hasNext():
        print loader.getNext()
    log = {'log':'MainMem Pages mapped read', 'score':2.25}
    loader.updateScore(log)
    
    
    
    
