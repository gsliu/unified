#!/usr/bin/python
import re
import os
import sys
import mimetypes
import enchant
import MySQLdb
from threading import Thread

sys.path.append('.')

#from istext import istext 
from lib.dbConn import getQueryUnified

class LogClip():
 
    def initDb(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.dictus = enchant.Dict("en_US")
        self.dictgb = enchant.Dict("en_GB")

    def __init__(self, table='logclip'):
        self.initDb()
        self.table = table

    def insertLog(self, log):
        sql = ("select * from %s where log = \"%s\" ")  % (self.table, log)
        query = getQueryUnified()
        query.Query(sql)
        data = query.record

        if len(data) > 0:
            print '      ignore ---->%s' % log
            return
   
        sql = ("INSERT INTO %s (log) VALUES ( \"%s\" )")  % (self.table, log)
        query = getQueryUnified()
        query.Query(sql)
   
        print("      insert----> %s") % log
   

    def isqualified(self, log):
        #if no charactor in the log drop it.
        try:
            cre = re.compile(r'[a-zA-Z]')
            if cre.search(log) is None:
                return False

            #check length
            if len(log) < 8:
                return False

            #dict check
            if self.dictus.check(log) or self.dictgb.check(log):
                return False
            return True
        except:
            return False


    def saveLog(self, log):
        #to lower
        log = log.lower()
       
        #trim special char in front and at the end of log
        #cset = []
        #for c in xrange(ord('a'), ord('z')+1):
        #    cset.append(chr(c))
        #some function is named as ___xxxx
        #cset.append('_')

        #while log and log[0] not in cset:
        #    log = log[1:]

        #while log and log[-1] not in cset:
        #    log = log[:-1]

        #insert the log
        if log and self.isqualified(log):
            log = MySQLdb.escape_string(log)
            self.insertLog(log)

if __name__ == '__main__':
    #runset = sys.argv[1].split(';')
    lp = LogClip('logclip')
    lp.saveLog('aaageGgsheng_aaaasdf--')
    lp.saveLog('geGgsheng----')
    lp.saveLog('_____geGgsheng.....')
     
