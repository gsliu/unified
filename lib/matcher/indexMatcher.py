import sys
import os
import threading

from lib.indexer.indexSearch import IndexSearch
from lib.symptom import Symptom
from lib.matcher.matcher import Matcher
from lib.indexer.indexLogs import IndexLogs
from lib.matcher.filterResult import filterResult


isearch = IndexSearch()

class searchThread(threading.Thread):
    def __init__(self,id, threadnumber, symptoms, ret, index):
        threading.Thread.__init__(self)
        self.id = id
        self.threadnumber = threadnumber
        self.symptoms = symptoms
        self.ret = ret
        self.index = index

    def run(self):
        j = 0
        for s in self.symptoms:
            j = j + 1
            if j % self.threadnumber == self.id:
                #print "the thread (%d) is running" %(self.id)
                score = 0.0
                mln = 0 # matched log numbers
                logs = []
                for log in s.getLogs():
                    if log['score']  > 0.3 and isearch.search( log['log'], self.index):
                        log['matched'] = 1
                        score = score + log['score']
                        mln = mln + 1
                        logs.append(log)
                    else:
                        log['matched'] = 0

                if mln > 0:
                    self.ret.append({'kbnumber':s.getKbnumber(), 'score':score, 'matchedlog':mln, 'logs':logs})
        #thread.exit_thread()


class IndexMatcher(Matcher):

    def getSymptoms(self):
        return self.symptoms

    def match(self, index, minlogscore, size=10, minscore=0.5, threadnumber=4):
        ret = []
        i = 0
        threads = []

        while i < threadnumber:
            threads.append(searchThread(i, threadnumber, self.symptoms, ret, index))
            i = i + 1
            #threads.append(threading.Thread(target=thread_main, args=(10,)))
            #thread.start_new_thread( self.run, (i, threadnumber, self.symptoms, ret)
        for t in threads:
            t.start() 

        for t in threads:
            t.join()

        ret = filterResult(ret, size, minscore)
        return ret


if __name__ == '__main__':
    m = IndexMatcher()
    inde = IndexLogs('/data/Min/unified/common/logs', "task1066")
    ret = m.match('task1066', 0.3)
    print ret
    #print ret 
    #ret = m.match("YYYY-MM-DDT18:05:57.433Z [3DF03B90 info 'Vcsvc.VMotionSrc (1388772268136447)'] ResolveCb: VMX reports needsUnregister = false for migrateType MIGRATE_TYPE_VMOTION")
    #print ret
    #ret = m.match("YYYY-MM-DDT18:04:27.748Z [4FA40B70 warning 'Vcsvc.VMotionDst (1388772268136447)' opID=57C757C9-000004C9-9c-75-89 user=vpxuser] Bind: Failed to initialize VMotionWorker")
    #f = open('log')
    #ret = m.match(f.read())
    #for r in ret:
    #    print "%s, %2.8f" % (r['kbnumber'], r['score'])
    #print ret
