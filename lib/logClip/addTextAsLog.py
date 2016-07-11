import re
import sys
import json
sys.path.append('.')

from subprocess import PIPE
from subprocess import Popen
from lib.logClip.logClip import LogClip

class AnalyzeText:
    def __init__(self):
        self.lc = LogClip()
         

    def parseResult(self, ret):
        kbs = []
        if 'hits' in ret:
            for hit in ret['hits']['hits']:
                kbs.append(int(hit['_id']))
	return kbs

        
    def analyze(self, text):
        ans = []
        data = '{"analyzer" : "space","text" : "%s"}' %(text)
        es_url = "http://localhost:9200/kb/_analyze"
        child = Popen(["curl", es_url, "-d", data, "-XPOST"], stdout=PIPE)
        res = child.communicate(None)[0]
        print res
        jres = json.loads(res)
        
        for token in jres['tokens']:
            print token['token']
            self.lc.saveLog(token['token'])

if __name__ == '__main__':
    at = AnalyzeText()
    at.analyze('gengshengl wang')
