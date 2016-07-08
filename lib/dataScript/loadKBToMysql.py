#!/usr/bin/python 

from datetime import datetime
from webpage import IKBPage
from os import listdir
from os.path import isfile, join
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class IKB_to_Mysql_Loader:

##############################################################################
# RedHat Database structure:
#    KBid, URL, Symptoms, Resolution, Solution, Details, Purpose, Cause, Title
#    search fields name in es: 
#       merge fields "symptoms, resolution, solution, details, purpose, cause" into text
##############################################################################

    def __init__(self, dir):
        self.conn = MySQLdb.connect(host= "localhost",
                      user="root",
                      passwd="vmware",
                      db="unified")
    	self.cursor = self.conn.cursor()
	self.kb_dir = dir
    #    self.create_index()      
    

    def save_item(self, page):
	doc = ( 
	    MySQLdb.escape_string(page.get_id()), 
            MySQLdb.escape_string(page.get_url()), 
	    MySQLdb.escape_string(page.get_title()), 
	    MySQLdb.escape_string(page.get_symptoms()), 
            MySQLdb.escape_string(page.get_resolution()), 
            MySQLdb.escape_string(page.get_solution()), 
            MySQLdb.escape_string(page.get_cause()), 
            MySQLdb.escape_string(page.get_purpose()), 
            MySQLdb.escape_string(page.get_details()) 
	) 

	print 'DEBUG: indexed kb ' + str(page.get_id())

	add_kb = ("INSERT INTO kb "
              	"(id, url, title, symptoms, resolution, solution, cause, purpose, details) "
              	"VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\" )")  % doc
	add_kb = add_kb.encode('utf-8')


	print add_kb
	# Insert new employee
	self.cursor.execute(add_kb)
 	self.conn.commit()


    def save_all(self):
        # iter all kbs
        for f in listdir(self.kb_dir):
            print "DEBUG: %s" %(f)
            file = join(self.kb_dir, f)
            if isfile(file):
                self.save_item(IKBPage(file))

    def done(self):
	self.conn.commit()
	self.cursor.close()
	print "Done" 

if __name__ == "__main__":
    #import sys
    #print len(sys.argv)
    #if len(sys.argv) < 2:
    #    print "Please provide KB dirname"
    #    exit(0)
    
    #loader = IKB_to_ES_Loader(sys.argv[1])
    loader = IKB_to_Mysql_Loader('./data')

    loader.save_all()
    loader.done()
