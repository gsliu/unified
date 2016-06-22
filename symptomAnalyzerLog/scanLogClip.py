#!/usr/bin/python
import re
import os
import mysql.connector
import sys
import MySQLdb
import mimetypes
import enchant
from istext import istext 
import thread

class ScanCodeClip():
 
    def initDb(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.cnx =  mysql.connector.connect(user='root', password="vmware", database='unified',  buffered = True)
        self.cursor = self.cnx.cursor()
        self.dictus = enchant.Dict("en_US")
        self.dictgb = enchant.Dict("en_GB")

    def __init__(self, dirname, table):
        self.dirname = dirname
        self.initDb()
        self.table = table

    def savelog(self, log):
        query_log = ("select * from %s where log = \"%s\" ")  % (self.table, log)
   
        #print query_log
        self.cursor.execute(query_log)
        row = self.cursor.fetchone()
        if row is not None:
            print 'ignore ---->%s' % log
            return
   
        add_log = ("INSERT INTO %s"
                     "(log) "
                     "VALUES ( \"%s\" )")  % (self.table, log)
   
        print("insert----> %s") % log
        self.cursor.execute(add_log) 
        self.cnx.commit()
   

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
        #p = re.compile("(%[^-\s]+)|%")
        #print log
        #ignore include
        postfix = re.compile(r'\.(?:h|c|cpp|java|cs)$')
        m = postfix.findall(log) 
        if m:
            return

        p = re.compile("(%[^-\s]+)|%$|'")
        splog = p.split(log)
        for slog in splog:
            if slog is None:
                continue
            #remove \n \t...
            slog = re.sub(r'\\[^-\s]', '', slog)
	    #remove \
            slog = re.sub(r'\\', '', slog)
            #remove # 
            log = re.sub(r'%', '', log)
   

            #escape the '"
            slog = MySQLdb.escape_string(slog)

            if slog and self.isqualified(slog):
                #strip the log
                log = log.strip()
                #print ('***' + slog)
                self.savelog(slog)
       


   
    def readandfindlog(self, filename):
        #f = open('/mnt/dbc/gengshengl/src/vsphere60p03/bora/vmx/main/main.c', 'r')
        f = open(filename, 'r')
        line = f.read();

        pattern = re.compile(r'"(\s*(.*?)\s*)"');

        matchObj = pattern.findall(line)

        if matchObj:
            for string in matchObj:
                self.process(string[0])

    def issourcecode(self, filename):
        #postfix = re.compile(r'"\.(h|c|cpp|java|cs)$"')
        postfix = re.compile(r'\.(?:h|c|cpp|java|cs)$')
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

    def closeDb(self): 
        self.cnx.commit()
        self.cnx.close()
if __name__ == '__main__':
    #runset = sys.argv[1].split(';')
    #loaddir("/mnt/dbc/gengshengl/src/vsphere60p03/bora/vmx")  

    runset = []
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/vmx')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/apps')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/lib')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/vmkernel')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/modules')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/devices')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/mks')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/cim')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/vim')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/vpx')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/public')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/ui')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora-soft')
    #runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/vmcore')
    runset.append('/mnt/dbc/gengshengl/src/vsphere60p03/bora/')
    #runset.append('/mnt/dbc/gengshengl/src/view623/mojo/')

    sccs = []  
    for s in runset:
        sccs.append(ScanCodeClip(s, 'logclip'))

    for scc in sccs:
        print 'starting new ....'
        thread.start_new_thread(scc.run,())
    while True:
        pass
