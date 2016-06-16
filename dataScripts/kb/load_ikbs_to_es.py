#!/usr/bin/python 

from datetime import datetime
from elasticsearch import Elasticsearch
from webpage import IKBPage
from os import listdir
from os.path import isfile, join

class IKB_to_ES_Loader:

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

    def index_item(self, page):
	doc = {
            'url': page.get_url(),
            'summary': page.get_title(),
            'symptoms': page.get_symptoms(),
            'resolution' : page.get_resolution(),
      	    'solution' : page.get_solution(),
      	    'cause' : page.get_cause(),
       	    'purpose': page.get_purpose(),
            'details': page.get_details(),
            'tags':page.get_tags()
        }
        res = self.es.index(index = self.index, doc_type = self.doc_type, id = page.get_id(), body = doc)
	#print 'DEBUG: indexed kb ' + str(page.get_id())
        return res['created']

    def index_all(self):
        # iter all kbs
        i = 0 
        for f in listdir(self.kb_dir):
            i = i + 1
            print " %d DEBUG: %s" %(i, f)
            file = join(self.kb_dir, f)
            if isfile(file):
                kb = IKBPage(file)
                tags = kb.get_tags()
                if 'Chinese' in tags or 'Japanese' in tags or 'Spanish' in tags or 'Portugues' in tags:
                    print 'ignore other langurage kb %s' % kb.get_id()
                    continue
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
