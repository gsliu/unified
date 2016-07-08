#!/usr/bin/python 

from datetime import datetime
from elasticsearch import Elasticsearch
from os import listdir
from os.path import isfile, join
import sys

sys.path.append('.')

from lib.kb.kbPage import KBPage

class KBESLoader:

##############################################################################
# RedHat Database structure:
#    KBid, URL, Symptoms, Resolution, Solution, Details, Purpose, Cause, Title
#    search fields name in es: 
#       merge fields "symptoms, resolution, solution, details, purpose, cause" into text
##############################################################################

    def __init__(self, dir):
        self.es = Elasticsearch()
        self.index = 'kb'
        self.doc_type = 'text'
        self.kb_dir = dir 
        self.createIndex()      
    
    def createIndex(self): 
        # Create an index with settings and mapping, a line is a term
        #    1. add a new tokenizer which divide by /n
        #    2. add mappings to doc_type and field
        doc = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "line": {
                            "type": "pattern",
                            "pattern": "[\n]+",
                        }
                    }
                }
            },
            'mappings':{
                self.doc_type:{
                   'properties':{
                        'text':{
                            'type':'string',
                            'index': 'analyzed',
                            'analyzer': 'line',
                            'search_analyzer': 'line',
                            #'analyzer':'line'
                        },                                      
                   } 
                } 
            }
        }
        #delete index first
        ret = self.es.indices.delete(index=self.index, ignore=[400, 404])
        res = self.es.indices.create(index=self.index, body=doc)
        return res    
        
    def indexItem(self, page):
	doc = {
            #'text':page.getIndexText()
            'text':page.getFullText()
        }
        #print doc
        res = self.es.index(index = self.index, doc_type = self.doc_type, id = page.getKbnumber(), body = doc)
        #print res 
        return res['created']

    def indexAll(self):
        # iter all kbs
        i = 0 
        for f in listdir(self.kb_dir):
            i = i + 1
            print " %d DEBUG: %s" %(i, f)
            file = join(self.kb_dir, f)
            if isfile(file):
                page = KBPage(int(f))
                tags = page.getTags()
                if 'Mandarin' in tags  or 'Chinese' in tags or 'Japanese' in tags or 'Spanish' in tags or 'Portugues' in tags:
                    print 'ignore other langurage kb %s' % page.getKbnumber()
                    continue
                self.indexItem(page)

if __name__ == "__main__":
    #import sys
    #print len(sys.argv)
    #if len(sys.argv) < 2:
    #    print "Please provide KB dirname"
    #    exit(0)
    
    #loader = IKB_to_ES_Loader(sys.argv[1])
    loader = KBESLoader('/data/kbdata')
    page = KBPage(2051492)
    page = KBPage(2097684)
    loader.indexItem(page)
    #loader.indexAll()
