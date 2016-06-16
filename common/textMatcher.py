import sys
import os
import mysql.connector
import MySQLdb


#print(sys.path)

from symptom import Symptom
from matcher import Matcher



class TextMatcher(Matcher):

    def getSymptoms(self):
        return self.symptoms

    def match(self, text):
        ret = []
        for s in self.symptoms:
            
            score = 0.0 
            mln = 0
            for log in s.getLogs():
                if log['log'] in text:
		    score = score + log['score']
                    mln = mln + 1
            if mln > 0:
                ret.append({'kbnumber':s.getKbnumber(), 'score':score, 'matchedlog':mln})
        return ret
       
                
                    
            


if __name__ == '__main__':
    m = TextMatcher()
    #sym = m.getSymptoms()
    ret = m.match("YYYY-MM-DDT18:05:57.424Z [3DF03B90 info 'Hostsvc.HaHost'] vmxSwapEnabled = true vmmOvhd.anonymous: 22964 vmmOvhd.paged: 63957 vmmOvhd.nonpaged: 13771")
    #print ret 
    ret = m.match("YYYY-MM-DDT18:05:57.433Z [3DF03B90 info 'Vcsvc.VMotionSrc (1388772268136447)'] ResolveCb: VMX reports needsUnregister = false for migrateType MIGRATE_TYPE_VMOTION")
    #print ret
    ret = m.match("YYYY-MM-DDT18:04:27.748Z [4FA40B70 warning 'Vcsvc.VMotionDst (1388772268136447)' opID=57C757C9-000004C9-9c-75-89 user=vpxuser] Bind: Failed to initialize VMotionWorker")
    #f = open('log')
    #ret = m.match(f.read())
    #for r in ret:
     #   print "%s, %2.8f" % (r['kbnumber'], r['score'])
    #print ret
