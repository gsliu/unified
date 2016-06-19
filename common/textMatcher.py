import sys
import os
import re
import mysql.connector
import MySQLdb

from filterResult import filterResult

#import filterResult

#print(sys.path)

#from symptom import Symptom
from matcher import Matcher
from symptomHits import SymptomHits

sh = SymptomHits()

class TextMatcher(Matcher):

    #core matchting algorithm
    def match(self, text, size=10, minscore=0.5):
        ret = []
        for s in self.symptoms:
            
            score = 0.0 
            mln = 0
            logs = []
            for log in s.getLogs():
                if log['log'] in text:
                    log['matched'] = 1
		    score = score + log['score']
                    mln = mln + 1
                else:
                    log['matched'] = 0
                
                logs.append(log)

            if mln > 0:
                ret.append({'kbnumber':s.getKbnumber(), 'score':score, 'matchedlog':mln, 'logs':logs})

        #update hits
        fret = filterResult(ret, size, minscore)
        for r in fret:
            sh.hit(r['kbnumber'])


        print fret
        return fret
       
                
                    
            


if __name__ == '__main__':
    m = TextMatcher(10.0)
    #sym = m.getSymptoms()
    ret = m.match("YYYY-MM-DDT18:05:57.424Z [3DF03B90 info 'Hostsvc.HaHost'] vmxSwapEnabled = true vmmOvhd.anonymous: 22964 vmmOvhd.paged: 63957 vmmOvhd.nonpaged: 13771")
    #print ret 
    ret = m.match("YYYY-MM-DDT18:05:57.433Z [3DF03B90 info 'Vcsvc.VMotionSrc (1388772268136447)'] ResolveCb: VMX reports needsUnregister = false for migrateType MIGRATE_TYPE_VMOTION")
    #print ret
    ret = m.match("YYYY-MM-DDT18:04:27.748Z [4FA40B70 warning 'Vcsvc.VMotionDst (1388772268136447)' opID=57C757C9-000004C9-9c-75-89 user=vpxuser] Bind: Failed to initialize VMotionWorker")
    #print ret
    #f = open('log')
    #ret = m.match(f.read())
    #for r in ret:
     #   print "%s, %2.8f" % (r['kbnumber'], r['score'])
    #print ret
