import os
import thread
import re 
import sys

from lib.indexer.indexLogs import IndexLogs
from logExtractor import esxiLogExtractor
 
from lib.dbConn import getQueryUnified
 
 
def queryTask( id): 
    sql = 'SELECT status from task where id = %d' % id
    query = getQueryUnified()
    query.Query(sql)
    data = query.record
 
    if data:
        return int(data[0]['status'])
    return None

def insertTask() :
    sql = 'SELECT max(id) as mid from task'
    query = getQueryUnified()
    query.Query(sql)
    data = query.record

    id = int(data[0]['mid']) + 1
    sql = 'INSERT INTO `task`(`id`, `status`) VALUES ( %d, %d)' % (id, 0)
    print sql
    query = getQueryUnified()
    query.Query(sql)


    return id


def updateTask( id, status):
    sql = 'UPDATE `task` SET `status`= %d  WHERE id = %d' % (status, id)
    query = getQueryUnified()
    query.Query(sql)

def createTask():
    id = insertTask()
    #mkdir /data/data/bundle/task<id>
    os.mkdir('/data/data/bundle/task%d'% id)
    return id

def startTask(id):
    dirname = '/data/data/bundle/task%d' % id
    indexname = 'task%d' %id
    #extract log
    
    print 'Extracting....%d' % id 
    esx = esxiLogExtractor('/data/data/bundle/task%d/' % id)
    ret = esx.extractAllFiles()

    print 'indexing task... %d' % id
    il = IndexLogs(dirname, indexname)
    
    print 'finished task... %d' %id
    updateTask(id, 1)

#def startTask(id):
#    thread.start_new_thread ( runTask, (id,) )
    


if __name__ == '__main__':
    #startTask(id)
    #id = insertTask()
    #print id
    id = createTask()
    print id
    s = queryTask(id)
    print s
    #startTask(1068)
    
    #while 1:
    #    print 'done'
        #pass 
