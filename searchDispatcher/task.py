import os
import thread
import re 
import mysql 
import mysql.connector 
 
 
 
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
    print 'running task %d' % id

def startTask(id):
    thread.start_new_thread ( runTask, (id,) )
    


if __name__ == '__main__':
    id = insertTask() 
    print id
    print queryTask(id)
    updateTask(id, 1)
    print queryTask(id)
    print queryTask(1004)
    id = createTask()
    startTask(id)
    id = createTask()
    startTask(id)
    id = createTask()
    startTask(id)
    id = createTask()
    startTask(id)
    
    while 1:
        pass 
