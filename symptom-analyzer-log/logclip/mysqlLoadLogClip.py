import re
import mysql
import mysql.connector



class MysqlLoadLogClip:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        self.cursor = self.cnx.cursor()
        self.cursor.execute('SELECT log FROM `logsrc` ')
        self.data = self.cursor.fetchone()

    def getNext(self):
        if self.data:
            olddata = self.data
            self.data = self.cursor.fetchone()
            return olddata[0]
            #return olddata
        return None

    def hasNext(self):
        if self.data:
            return True
        return False


if __name__ == '__main__':
    loader = MysqlLoadLogClip()
    while loader.hasNext():
        print loader.getNext()
    
    
    
    
