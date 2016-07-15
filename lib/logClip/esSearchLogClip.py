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
        #res = self.es.search(index='kb', q='" ' + log + ' "', size=30) 
        #res = self.es.search(index='kb', q=log, size=30) 
        #res = self.es.search(index="kb",  body={"query":{ "regexp": {"text": log }}}, size=30)
      

        #test shows that symbol will not be ignored using match_phrase 
        doc = {
            "query": {
                "match_phrase": {
                    "text": log
                }
            }
        }
        res = self.es.search(index="kb",  body=doc, size=30)
        return res

if __name__ == '__main__':
    eslog = ESSearchLogClip()
    #kbs = eslog.search('and try again.')    
    #kbs = eslog.search('<?xml version=\\')    
    kbs = eslog.search('domain\\\user')    
    #kbs = eslog.search(".*snapshot.*")    
    #kbs = eslog.search(".*.* artificial lock failure induced on .*.*")    
    #kbs = eslog.search(".* Invalid .* value \(.* using .*")    
    print eslog.parseResult(kbs)
