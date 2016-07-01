import sys

sys.path.append('.') 

from lib.dbConn import getQueryUnified
     
class MysqlLogClip:
    def __init__(self, table):
        self.table = table
        sql = 'SELECT log, score FROM %s ' % self.table
        query = getQueryUnified()
        query.Query(sql)
        self.data = query.record

	self.i = 0

    def getNext(self):
        if self.i < len(self.data):
            row = self.data[self.i]
            self.i = self.i + 1
            return {'log':row['log'], 'score':row['score']}

        return None

    def hasNext(self):
        if self.i < len(self.data):
            return True
        return False
    def getTable(self):
        return self.table
    
    def updateScore(self, log):
        sql = ('UPDATE %s SET `score`=%2.8f WHERE log = "%s"') % (self.table, log['score'], log['log'])
	print sql
        query = getQueryUnified()
        query.Query(sql)




if __name__ == '__main__':
    loader = MysqlLogClip('logclip')
    #while loader.hasNext():
    #    print loader.getNext()
    log = {'log':'MainMem Pages mapped read', 'score':0.25}
    loader.updateScore(log)
    
    
    
    
