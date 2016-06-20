import os
import thread
import re 
import mysql 
import mysql.connector 
import sys
sys.path.append('..')
from common.indexLogs import IndexLogs
 
 
 
def queryTask( id): 
    cnx = mysql.connector.connect(user='root',password='vmware', database='unified') 
    cursor = cnx.cursor() 
    cursor.execute('SELECT status from task where id = %d' % id) 
    data = cursor.fetchall() 
 
    cnx.close()
    if data:
        return int(data[0][0])
    return None

def insertTask() :
    cnx = mysql.connector.connect(user='root',password='vmware', database='unified') 
    cursor = cnx.cursor() 
    cursor.execute('SELECT max(id) from task' ) 
    data = cursor.fetchall() 
    id = int(data[0][0]) + 1
    cursor.execute('INSERT INTO `task`(`id`, `status`) VALUES ( %d, %d)' % (id, 0))
    cnx.commit()
    cnx.close()
    return id


def updateTask( id, status):
    cnx = mysql.connector.connect(user='root',password='vmware', database='unified') 
    cursor = cnx.cursor() 
    cursor.execute('UPDATE `task` SET `status`= %d  WHERE id = %d' % (status, id))
    cnx.commit()
    cnx.close()

def createTask():
    id = insertTask()
    #mkdir /data/data/bundle/task<id>
    os.mkdir('/data/data/bundle/task%d'% id)
    return id

def runTask(id):
    dirname = '/data/data/bundle/task%d' % id
    indexname = 'task%d' %id
    il = IndexLogs(dirname, indexname)
    print 'indexing task... %d' % id

def startTask(id):
    thread.start_new_thread ( runTask, (id,) )
    


if __name__ == '__main__':
    #startTask(id)
    #id = createTask()
    startTask(1066)
    
    while 1:
        print 'done'
        pass 
