import sys
import os
import threading
sys.path.append('.')

from lib.symptom import Symptom
from lib.matcher.matcher import Matcher



class SearchThread(threading.Thread):
    def __init__(self,id, threadnumber, symptoms, ret, text, minscore):
        threading.Thread.__init__(self)
        self.id = id
        self.threadnumber = threadnumber
        self.symptoms = symptoms
        self.ret = ret
        self.text = text
        self.minscore = minscore

    def run(self):
        i = self.id
        while i < len(self.symptoms):
            score = 0.0
            mln = 0
            for log in self.symptoms[i].getLogs():
                if log['log'] in self.text:
                    score = score + log['score']
                    mln = mln + 1
            if mln > 0 and score > self.minscore:
                self.ret.append({'symptom':self.symptoms[i], 'score':score})
                pass
            i = i + self.threadnumber

        print 'End thread %d, size= %d' % (self.id, len(self.ret))
                
class TextMatcher(Matcher):

    def match(self, text, size=10, minscore=0.5, threadnumber=8):
        text = text.lower()
        ret = []
        i = 0
        threads = []

        while i < threadnumber:
            threads.append(SearchThread(i, threadnumber, self.symptoms, ret, text, minscore))
            i = i + 1

        for t in threads:
            t.start() 

        for t in threads:
            t.join()

        if ret == None:
            return ret

        print 'total = %d' % len(ret)

        ret.sort(key=lambda x: x['score'], reverse=True)

        if ret and len(ret) > 30:   
            ret = ret[0:30]
        fs = []
        for r in ret:
            fs.append(r['symptom'])

        ret = self.cf.computeClusterScore(text, fs, size, minscore)
     
        return ret


if __name__ == '__main__':
    m = TextMatcher(10)
    ret = m.match("YYYY-MM-DDT18:05:57.433Z [3DF03B90 info 'Vcsvc.VMotionSrc (1388772268136447)'] ResolveCb: VMX reports needsUnregister = false for migrateType MIGRATE_TYPE_VMOTION")
    print ret
    ret = m.match("YYYY-MM-DDT18:04:27.748Z [4FA40B70 warning 'Vcsvc.VMotionDst (1388772268136447)' opID=57C757C9-000004C9-9c-75-89 user=vpxuser] Bind: Failed to initialize VMotionWorker")
    #f = open('log')
    #ret = m.match(f.read())
    #for r in ret:
    #    print "%s, %2.8f" % (r['kbnumber'], r['score'])
    print ret
