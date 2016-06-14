#!/usr/bin/python
import re
import os
import mysql.connector
import sys
import MySQLdb
import mimetypes
import enchant
from istext import istext 
def init_db():
   reload(sys)
   sys.setdefaultencoding('utf-8')
   global cnx 
   cnx =  mysql.connector.connect(user='root', password="vmware", database='unified',buffered = True)
   global cursor 
   cursor = cnx.cursor()
   global dictus
   dictus = enchant.Dict("en_US")
   global dictgb
   dictgb = enchant.Dict("en_GB")

def savelog(log):
   query_log = ("select * from logsrc where log = \"%s\" ")  % log
   
   #print query_log
   cursor.execute(query_log)
   row = cursor.fetchone()
   if row is not None:
       print 'ignore ---->%s' % log
       return
   
   add_log = ("INSERT INTO logsrc"
                "(log) "
                "VALUES ( \"%s\" )")  % log
   
   print("insert----> %s") % log
   cursor.execute(add_log) 
   cnx.commit()
   

def isqualified(log):
    #if no charactor in the log drop it.
    cre = re.compile(r'[a-zA-Z]')
    if cre.search(log) is None:
        return False

    #check length
    if len(log) < 10:
        return False

    #dict check
    
    if dictus.check(log) or dictgb.check(log):
        return False
    return True
 
def process(log):
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

        if slog and isqualified(slog):
            #strip the log
            log = log.strip()
            #print ('***' + slog)
            savelog(slog)
   


   
def readandfindlog(filename):
    #f = open('/mnt/dbc/gengshengl/src/vsphere55u3/bora/vmx/main/main.c', 'r')
    f = open(filename, 'r')
    line = f.read();

    pattern = re.compile(r'"(\s*(.*?)\s*)"');

    matchObj = pattern.findall(line)

    if matchObj:
        for string in matchObj:
            process(string[0])

def issourcecode(filename):
    #postfix = re.compile(r'"\.(h|c|cpp|java|cs)$"')
    postfix = re.compile(r'\.(?:h|c|cpp|java|cs)$')
    m = postfix.findall(filename) 
    if m:
        return True
    return False

def loaddir(dirname):
    for root, dirs, files in os.walk(dirname):
        path = root.split('/')
        #print((len(path) - 1) * '---', os.path.basename(root))
        #print root
        for file in files:
            filename = root + '/' + file
           # print filename
            if issourcecode(file):
            #if istext(filename) and issourcecode(filename):
                print('processting file=============>>>> ' + filename)
                readandfindlog(filename)

def close_db(): 
    cnx.commit()
    cnx.close()

if __name__ == '__main__':
    init_db()
    loaddir(sys.argv[1])  
    #loaddir("/mnt/dbc/gengshengl/src/vsphere55u3/bora/vmx")  
    close_db()
