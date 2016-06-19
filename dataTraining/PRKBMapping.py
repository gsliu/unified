from datetime import datetime
from elasticsearch import Elasticsearch
from os import listdir
from os.path import isfile, join
import sys
from threading import Thread
import config

sys.path.append('..')
from dataScripts.bz.db_bz import *



class KBPRLoader:

##############################################################################
# VMBugzilla Database structure: 
#    bugid(0), title(9), text(11) (essential part for full text search)
#       opened(1), severity(2), priority(3), status(4), assignee(5), reporter(6),
#       category(7), component(8), fixby(10)(for result display)
#   fields name is es:
#       summary, text       
##############################################################################

    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'bugzilla'
        self.doc_type = 'text'
        self.working_thread = []
        #self.create_index()
    
    def create_index(self, bug_id): 
        # Create an index with settings and mapping, a line is a term
        #    1. add a new tokenizer which divide by /n
        #    2. add mappings to doc_type and field
        doc = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'whilespace':{
                            'type':'pattern',
                            'pattern':'\n'
                        }
                    }
                }
            },
            'mappings':{
                self.doc_type:{
                   'properties':{
                        'summary':{
                            'type':'string',
                            'analyzer':'whitespace'
                        },                                       
                        'comment':{
                            'type':'string',
                            'analyzer':'whitespace'
                        }                                       
                    } 
                } 
            }
        }
        res = self.es.indices.create('bz%d' % bug_id, body = doc)
        print 'create index for PR %d' % bug_id
        return res    

    def get_bug_list(self):
        sql='select unique(bug_id) from bug_kb_mapping '
        bz_cur.execute(sql)
        item = bz_cur.fetchall()
        bugs = []
        for row in item:
            bugs.append(row[0])
        return bugs

    def get_comments(self, bug_id):
        sql = 'select thetext from longdescs where bug_id = ' % bug_id
        item = bz_cur.fetchall()
        comments = []
        for row in item:
            comments.append(row[0])
        return comments

    def get_summary(self, bug_id):
        sql = 'select summary from bugs where bug_id = ' % bug_id
        item = bz_cur.fetchall()
        return item[0][0]



    def index_summary(self, bug_id, summary ):
        doc = {
            # title seems to be a reversed filed, change to summary
            'summary': summary,
        }
        #print doc
        res = self.es.index('bz%d' % bug_id, doc_type = self.doc_type, id = 0, body = doc)
        return res

    def index_comment(self, bug_id, comment, c_id):
        doc = {
            'comment': comment,
        }
        #print doc
        res = self.es.index('bz%d' % bug_id, doc_type = self.doc_type, id = c_id, body = doc)
        return res

    def index_all(self):
        bugs = self.get_bug_list()
        for bug_id in bugs:
            self.create_index(bug_id)
            index_summary(bug_id, self.get_summary(bug_id))
            c_id = 0
            for comment in self.get_comments(bug_id):
                c_id = c_id + 1
                self.index_comment(bug_id, comment, c_id)
            
            


if __name__ == "__main__":
    import sys
    
    loader = KBPRLoader()

    #print loader.create_item(1291688)
    #print loader.create_item(1335744)
    #print loader.create_item(1339158)
    loader.index_all()
