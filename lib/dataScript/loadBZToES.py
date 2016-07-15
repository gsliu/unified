from elasticsearch import Elasticsearch
from threading import Thread
import sys
sys.path.append('.')

from lib.bug.bug import Bug
from lib.dbConn import getQueryBugzilla


begin = 1

class BZESLoader:

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
        self.create_index()
    
    def create_index(self): 
        # Create an index with settings and mapping, a line is a term
        #    1. add a new tokenizer which divide by /n
        #    2. add mappings to doc_type and field
        doc = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "space": {
                            "type": "pattern",
                            "pattern": "[\s\n]+",
                        }
                    }
                }
            },
            'mappings':{
                self.doc_type:{
                   'properties':{
                        'summary':{
                            'type':'string',
                            'index': 'analyzed',
                            'analyzer': 'space',
                            'search_analyzer': 'space',
                        },
                        'text':{
                            'type':'string',
                            'index': 'analyzed',
                            'analyzer': 'space',
                            'search_analyzer': 'space',
                        },

                   }
                }
            }
        }
 
        ret = self.es.indices.delete(index=self.index, ignore=[400, 404])
        res = self.es.indices.create(index=self.index, body=doc)
        return res    

    def index_item(self, bug):
        doc = {
            # title seems to be a reversed filed, change to summary
            'summary': bug.getSummary(),
            'text': bug.getText(),
        }
        #print doc
        res = self.es.index(index = self.index, doc_type = self.doc_type, id = bug.getBugId(), body = doc)
        return res['created']

    def index_worker(self, low, high):
        
        for i in range(low, high):
            print "working:" + str(i)
            bug = Bug(i)
            self.index_item(bug)

    def index_all(self):
        # iter all
        sql = 'select max(bug_id) as max_id from bugs'
        query = getQueryBugzilla()
        query.Query(sql)
        data = query.record
        max_bugid = data[0]['max_id']
        print "max:" + str(max_bugid)
        end = max_bugid
        low = begin
        work_size = (end - begin) / 80
        high = min(low + work_size, end) 
        while low < high:
            t = Thread(target = self.index_worker, args = (low, high))
            t.start()
            low = high
            high = min(low + work_size, end)
            self.working_thread.append(t)
        for t in self.working_thread:
            t.join()

if __name__ == "__main__":
    
    loader = BZESLoader()

    #print loader.create_item(1291688)
    #print loader.create_item(1335744)
    #print loader.create_item(1339158)
    loader.index_all()
