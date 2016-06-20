import sys
import os
import mysql.connector
import MySQLdb
import pyes
from elasticsearch import Elasticsearch

class IndexSearch(object):
    def __init__(self):
        self.es = Elasticsearch()

    def search(self, log, indexname):        

        #conn = pyes.ES('http://unified.eng.vmware.com:9200')
        #query = pyes.TermQuery('logFileName', log)
        #query = pyes.StringQuery(log, 'logs')
        #query = pyes.search(index=indexname, q='"' + log + '"', size=20)
        res = self.es.search(index=indexname, q='"' + log + '"')  # add "" for log 

        if 'hits' in res:
            print 'There is matched result. ' + log
            return True
        
        return False

if __name__ == '__main__':
    s = IndexSearch()
    s.search('restore-bootbanks', "tast-indexname")