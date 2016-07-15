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
from lib.logClip.logClip import LogClip

class ScanString():
    def __init__(self, dirname, table):
        self.dirname = dirname
        self.lc = LogClip(table)

    def process(self, log):
        #to lower case
        log = log.lower()
         
        #remove \n 
        log = re.sub('\\n', '', log)
   
        print 'Found log -----> %s' % log
        #p = re.compile(r'[^-\s]{0,}%[^-\s]{0,}|\|\n|\t|\r')
        p = re.compile(r'\\[^-\s]{0,}|[^-\s]{0,}%[^-\s]{0,}')
        splog = p.split(log)
        for slog in splog:
            if slog:
                self.lc.saveLog(slog)
   
    def readandfindlog(self, filename):
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
        print "Src processing -----> %s" % self.dirname
        for root, dirs, files in os.walk(self.dirname):
            path = root.split('/')
            #print((len(path) - 1) * '---', os.path.basename(root))
            #print root
            for file in files:
                filename = root + '/' + file
                # print filename
                if self.issourcecode(file):
                #if istext(filename) and issourcecode(filename):
                    print('processting file--------->' + filename)
                    self.readandfindlog(filename)

def scanAll(runset):
    sccs = []  
    for s in runset:
        sccs.append(ScanString(s, 'logclip'))

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

