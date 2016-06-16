import re
import sys

from elasticsearch import Elasticsearch

class ESSearchLogClip:
    def __init__(self):
        self.es = Elasticsearch()
         

    def parseResult(self, ret):
        kbs = []
        if 'hits' in ret:
            for hit in ret['hits']['hits']:
                kbs.append(int(hit['_id']))
	return kbs

        
    def search(self, log):
        ret = self.es.search(index='ikb', q='"' + log + '"', size=30) 
        return ret
        #return self.parseResult(ret)

if __name__ == '__main__':
    eslog = ESSearchLogClip()
    kbs = eslog.search('and try again.')    
    kbs = eslog.search('ERROR_WAIT')    
    print eslog.parseResult(kbs)
