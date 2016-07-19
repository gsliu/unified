import sys
import os
import re
sys.path.append('.')




from lib.matcher.matcher import Matcher
from lib.symptomHits import SymptomHits

sh = SymptomHits()

class TextMatcher(Matcher):

    #core matchting algorithm
    def match(self, text, size=10, minscore=0.5):
        text = text.lower()
        hitSymptoms = []
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
                #ret.append({'kbnumber':s.getKbnumber(), 'score':score, 'matchedlog':mln, 'logs':logs})
                hitSymptoms.append(s)
        ret = self.cf.computeClusterScore(text, hitSymptoms, size, minscore)
        



        return ret

if __name__ == '__main__':
    m = TextMatcher(0.0)
    #sym = m.getSymptoms()
    text = "YYYY-MM-DDT18:05:57.424Z [3DF03B90 info 'Hostsvc.HaHost'] vmxSwapEnabled = true vmmOvhd.anonymous: 22964 vmmOvhd.paged: 63957 vmmOvhd.nonpaged: 13771\n"
    text = text + "YYYY-MM-DDT18:05:57.433Z [3DF03B90 info 'Vcsvc.VMotionSrc (1388772268136447)'] ResolveCb: VMX reports needsUnregister = false for migrateType MIGRATE_TYPE_VMOTION\n"
    text = text + "YYYY-MM-DDT18:04:27.748Z [4FA40B70 warning 'Vcsvc.VMotionDst (1388772268136447)' opID=57C757C9-000004C9-9c-75-89 user=vpxuser] Bind: Failed to initialize VMotionWorker\n"
    ret = m.match(text)
    print ret
    #f = open('log')
    #ret = m.match(f.read())
    #for r in ret:
     #   print "%s, %2.8f" % (r['kbnumber'], r['score'])
    #print ret

