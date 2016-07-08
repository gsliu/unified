#!/usr/bin/python
import re
import os
import sys
import mimetypes
import enchant
import MySQLdb
from threading import Thread

sys.path.append('.')

from istext import istext 
from lib.dbConn import getQueryUnified

class ScanCodeClip():
 
    def initDb(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.dictus = enchant.Dict("en_US")
        self.dictgb = enchant.Dict("en_GB")

    def __init__(self, dirname, table):
        self.dirname = dirname
        self.initDb()
        self.table = table

    def savelog(self, log):
        sql = ("select * from %s where log = \"%s\" ")  % (self.table, log)
        query = getQueryUnified()
        query.Query(sql)
        data = query.record

        if len(data) > 0:
            print 'ignore ---->%s' % log
            return
   
        sql = ("INSERT INTO %s (log) VALUES ( \"%s\" )")  % (self.table, log)
        query = getQueryUnified()
        query.Query(sql)
   
        print("insert----> %s") % log
   

    def isqualified(self, log):
        #if no charactor in the log drop it.
        try:
            cre = re.compile(r'[a-zA-Z]')
            if cre.search(log) is None:
                return False

            #check length
            if len(log) < 10:
                return False

            #dict check
    
            if self.dictus.check(log) or self.dictgb.check(log):
                return False
            return True
        except:
            return False
 
    def process(self, log):
        #strip the log
        #print log
        log = log.strip(' \t\n\r')
        log = re.sub(r'\\n', '', log)
        #print log 
        #escape the regex sympbol
        log = re.escape(log)
        #print log
        #replace % with .*
        log = re.sub("(%[^-\s]+)|%$|'", '.*', log)
        #log = re.sub(r'\\[^-\s]', '', log)
        #log = re.sub(r'\\', '', log)
        while log.startswith( '.*' ):
            log = log[2:]
            log = log.strip(' \t\n\r')
        while log.endswith( '.*' ):
            log = log[0:-2]
            log = log.strip(' \t\n\r')
        log = '.*' + log + '.*'

        log = MySQLdb.escape_string(log)

        if log and self.isqualified(log):
            #print ('***' + slog)
            self.savelog(log)
   


   
    def readandfindlog(self, filename):
        #f = open('/data/gengshengl/src/vsphere60p03/bora/vmx/main/main.c', 'r')
        f = open(filename, 'r')
        line = f.read();

        pattern = re.compile(r'"(\s*(.*?)\s*)"');

        matchObj = pattern.findall(line)

        if matchObj:
            for string in matchObj:
                self.process(string[0])

    def issourcecode(self, filename):
        #postfix = re.compile(r'"\.(h|c|cpp|java|cs)$"')
        postfix = re.compile(r'\.(?:h|c|cpp|java|cc|hpp|cs)$')
        m = postfix.findall(filename) 
        if m:
            return True
        return False

    def run(self):
        print "processing.. %s" % self.dirname
        for root, dirs, files in os.walk(self.dirname):
            path = root.split('/')
            #print((len(path) - 1) * '---', os.path.basename(root))
            #print root
            for file in files:
                filename = root + '/' + file
                # print filename
                if self.issourcecode(file):
                #if istext(filename) and issourcecode(filename):
                    print('processting file=============>>>> ' + filename)
                    self.readandfindlog(filename)

def scanAll(runset):
    sccs = []  
    for s in runset:
        sccs.append(ScanCodeClip(s, 'logclip'))

    threads = []
    for scc in sccs:
        print 'starting new ....'
        t = Thread(target=scc.run, args=())
        t.start()
        threads.append(t)
        #thread.start_new_thread(scc.run,())
    # join all threads
    for t in threads:
        t.join()

    print 'Done scaning the code'

if __name__ == '__main__':
    #runset = sys.argv[1].split(';')
    #loaddir("/data/gengshengl/src/vsphere60p03/bora/vmx")  

    runset = []
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/vmx')
    runset.append('/data/src/gengshengl/src/vsphere60p03/bora/apps')
    runset.append('/data/src/gengshengl/src/vsphere60p03/bora/lib')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/vmkernel')
    runset.append('/data/src/gengshengl/src/vsphere60p03/bora/modules')
    runset.append('/data/src/gengshengl/src/vsphere60p03/bora/devices')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/vmx/main/')
    #runset.append('/data/src/gengshengl/src/view623/mojo/')
    scanAll(runset)

