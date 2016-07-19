import re
import sys
import json
sys.path.append('.')

from subprocess import PIPE
from subprocess import Popen
from lib.logClip.logClip import LogClip
from lib.logClip.logClipFilter import kbLogFilter

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
        tokens = text.split()
        regex = r'[^A-Za-z0-9\-\_]'
        for token in tokens:
            logclips = re.split(regex, token)
            for logclip in logclips:
                self.lc.saveLog(logclip, kbLogFilter)

if __name__ == '__main__':
    at = AnalyzeText()
    at.analyze("verbose 'vm:/vmfs/volumes/4da7419d-76842557-1fe8-001a6468e1ed/erptlbi/erptlbi.vmx'] VMotionResolveCheck: Firing ResolveCb")
