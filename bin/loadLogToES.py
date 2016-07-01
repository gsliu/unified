#!/usr/bin/python 

from datetime import datetime
from elasticsearch import Elasticsearch
from webpage import IKBPage
from os import listdir
from os.path import isfile, join
from logCheckKBHtml import LogHTMLChecker

class IKB_to_ES_Loader:

##############################################################################
# RedHat Database structure:
#    KBid, URL, Symptoms, Resolution, Solution, Details, Purpose, Cause, Title
#    search fields name in es: 
#       merge fields "symptoms, resolution, solution, details, purpose, cause" into text
##############################################################################

    def __init__(self, dir):
        self.es = Elasticsearch()
        self.index = 'kblog'
        self.doc_type = 'log'
        self.kb_dir = dir 
        self.logchecker = LogHTMLChecker()
        self.create_index()      
    
    def create_index(self): 
        # Create an index with settings and mapping, a line is a term
        #    1. add a new tokenizer which divide by /n
        #    2. add mappings to doc_type and field
        doc = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'whitespace':{
                            'type':'pattern',
                            'pattern':'\n'
                        }
                    }
                }
            },
            'mappings':{
                self.doc_type:{
                   'properties':{
                                                              
			'log':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },




                    } 
                } 
            }
        }
        res = self.es.indices.create(index = self.index, body = doc)
        return res    

    def index_item(self, page):
        kblog = self.logchecker.getLog(page.get_id())
        if len(kblog) > 0:
	    doc = {
                'log': kblog,
            }
            res = self.es.index(index = self.index, doc_type = self.doc_type, id = page.get_id(), body = doc)
	    print 'DEBUG: indexed kb ' + str(page.get_id())
            return res['created']

    def index_all(self):
        # iter all kbs
        for f in listdir(self.kb_dir):
            print "DEBUG: %s" %(f)
            file = join(self.kb_dir, f)
            if isfile(file):
                self.index_item(IKBPage(file))

if __name__ == "__main__":
    #import sys
    #print len(sys.argv)
    #if len(sys.argv) < 2:
    #    print "Please provide KB dirname"
    #    exit(0)
    
    #loader = IKB_to_ES_Loader(sys.argv[1])
    loader = IKB_to_ES_Loader('/data/data/kbraw/data')

    loader.index_all()
