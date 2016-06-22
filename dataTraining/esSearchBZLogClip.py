import re
import sys

from elasticsearch import Elasticsearch

class ESSearchBZLogClip:
    def __init__(self):
        self.es = Elasticsearch()
         

    def parseResult(self, ret):
        bzs = []
        if 'hits' in ret:
            for hit in ret['hits']['hits']:
                bzs.append(int(hit['_id']))
	return bzs

        
    def search(self, log):
        ret = self.es.search(index='bugzilla', q='"' + log + '"', size=15) 
        return ret
        #return self.parseResult(ret)

if __name__ == '__main__':
    eslog = ESSearchBZLogClip()
    bzs = eslog.search('and try again.')    
    bzs = eslog.search('ERROR_WAIT')    
    print len(eslog.parseResult(bzs))
