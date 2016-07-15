import sys

sys.path.append('.') 

from lib.dbConn import getQueryUnified
     
class MysqlLogClip:
    def __init__(self, table):
        self.table = table
        sql = 'SELECT log FROM %s where scan = 0' % self.table
        query = getQueryUnified()
        query.Query(sql)
        self.data = query.record

	self.i = 0

    def getNext(self):
        if self.i < len(self.data):
            row = self.data[self.i]
            self.i = self.i + 1
            return {'log':row['log'], 'score': float(0.0)}

        return None

    def hasNext(self):
        if self.i < len(self.data):
            return True
        return False
    def getTable(self):
        return self.table
    
    def updateScan(self, log):
        sql = ('UPDATE %s SET `scan`= 1 WHERE log = "%s"') % (self.table,  log['log'])
	#print sql
        query = getQueryUnified()
        query.Query(sql)




if __name__ == '__main__':
    loader = MysqlLogClip('logclip')
    while loader.hasNext():
        print loader.getNext()
    #log = {'log':'MainMem Pages mapped read', 'score':0.25}
#    loader.updateScore(log)
    
    
    
    
