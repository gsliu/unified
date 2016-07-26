from datetime import datetime
from elasticsearch import Elasticsearch
from os import listdir
from os.path import isfile, join
import sys
sys.path.append('.')
print sys.path
from lib.matcher.textMatcher import TextMatcher
from lib.dbConn import getQueryUnified
from lib.dbConn import getQueryBugzilla
import thread


textMatcher = TextMatcher(0)


class EvaluateSearch:
    def getFullText(self, bugid):
       
        # generate thetext
        #    SQL: select group_concat(thetext) from longdescs group by bug_id limit %d,1' %(bugid)
        #       is too slow
        sql = 'set group_concat_max_len = 10240000'
        query = getQueryBugzilla()
        query.Query(sql)

        sql = 'select group_concat(thetext) as text from \
            (select thetext from longdescs where bug_id = %d) as myalias' %(bugid)
        query = getQueryBugzilla()
        query.Query(sql)
        data = query.record

        # add unicode to avoid json dumps error
        text = unicode(data[0]['text'], errors='replace')
        
        return text

    def testMatch(self, bug):
        text = self.getFullText(bug)
        print text
        print ret

    def process(self):
        pr_kb_sql = 'select min(bug_id) bug_id, kb_id from bug_kb_map group by kb_id'
        query = getQueryBugzilla()
        query.Query(pr_kb_sql)
        data = query.record

        pr_kb = []
        for d in data:
            m = {'pr':d['bug_id'], 'kb':d['kb_id']}
            pr_kb.append(m)

        sdict = {}
        sqlkb = 'select distinct kbnumber from symptom_log_cluster'
        query = getQueryUnified()
        query.Query(sqlkb)
        data = query.record

        for d in data:
            sdict[d['kbnumber']] = 1
      
        i = 0 
        mset = []
        r = []
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        r.append(0)
        print r

        tid = 0
        threadnumber = 1

        while tid < threadnumber:
            print 'starting thread %d.....' % tid
            thread.start_new_thread ( self.run, (r, tid, threadnumber, pr_kb, sdict) )
            tid = tid + 1


    def run(self, r, tid, threadnumber, pr_kb, sdict):
        loop = 0
        test = 0
        for pk in pr_kb:
            #oprint ('thread %d ' % tid).join(r)
            if loop % threadnumber == tid:
                if sdict.has_key(pk['kb']):
                    test = test + 1
                    print 'testing bug %s...' % pk['pr']
                    text = self.getFullText(pk['pr'])
                    ret = textMatcher.match(text)
                    if len(ret) != 0:
                        pos = 0
                        for re in ret:
                            if pos >= len(r) :
                                 break
                            if str(re['kbnumber']) == str(pk['kb']):
                                r[pos] = r[pos] + 1
                                print r
                                break
                            pos = pos + 1
                    else:
                        print '   no result for %s' % pk['pr']
            loop = loop + 1
            print 'done %d of %d, %d in the dict ... %s' % ( loop, len(pr_kb), test, str(r))




if __name__ == "__main__":
    ev = EvaluateSearch()
    ev.process()
    while True:
        pass
