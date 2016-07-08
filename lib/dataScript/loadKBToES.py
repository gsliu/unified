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
    #    self.create_index()      
    
    def createIndex(self): 
        # Create an index with settings and mapping, a line is a term
        #    1. add a new tokenizer which divide by /n
        #    2. add mappings to doc_type and field
        doc = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'whitespace':{
                            'type':'pattern',
                            'pattern':'[\n]+'
                        }
                    }
                }
            },
            'mappings':{
                self.doc_type:{
                   'properties':{
                                                              
                        'title':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },                                       
			'symptoms':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },
			'resolution':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },
			'solution':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },
			'purpose':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },
			'cause':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },
			'details':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },

			'tags':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },




                    } 
                } 
            }
        }
        res = self.es.indices.create(index = self.index, body = doc)
        return res    

    def indexItem(self, page):
	doc = {
            'url': page.getUrl(),
            'summary': page.getTitle(),
            'symptoms': page.getSymptoms(),
            'resolution' : page.getResolution(),
      	    'solution' : page.getSolution(),
      	    'cause' : page.getCause(),
       	    'purpose': page.getPurpose(),
            'details': page.getDetails(),
            'tags':page.getTags()
        }
        res = self.es.index(index = self.index, doc_type = self.doc_type, id = page.getKbnumber(), body = doc)
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

    loader.indexAll()
