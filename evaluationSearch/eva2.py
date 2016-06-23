from datetime import datetime
from elasticsearch import Elasticsearch
from os import listdir
from os.path import isfile, join
import thread
import sys
import mysql
import MySQLdb
sys.path.append('..')
print sys.path
from dataScripts.bz.db_bz import get_bz_con
from common.textMatcher import TextMatcher
from threading import Thread
import config

from threading import Thread, Lock
textMatcher = TextMatcher()
mutex = Lock()


bz_con, bz_cur = get_bz_con()
class EvaluateSearch:

##############################################################################
# VMBugzilla Database structure: 
#    bugid(0), title(9), text(11) (essential part for full text search)
#       opened(1), severity(2), priority(3), status(4), assignee(5), reporter(6),
#       category(7), component(8), fixby(10)(for result display)
#   fields name is es:
#       summary, text       
##############################################################################

    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'bugzilla'
        self.doc_type = 'text'
        #self.create_index()

    def create_item(self, bugid):
        sql='select bug_id, creation_ts, bug_severity, priority, bug_status, assigned_to, reporter, category_id, component_id, short_desc from bugs where bug_id = %d' %(bugid)
        bz_cur.execute(sql)
        item = bz_cur.fetchall()
    
        assert(len(item) == 1)
        ans = list(item[0])
       
        # handle title encode
        ans[9] = unicode(ans[9], errors='replace')
        # handle time
        ans[1] = str(ans[1]).split()[0]

        # replace userid by login_name  
        sql='select login_name from profiles where userid = %s' %(ans[5])
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        ans[5] = name[0][0]
   
        sql='select login_name from profiles where userid = %s' %(ans[6])
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        ans[6] = name[0][0] 
   
        # replace category_id by category name
        sql= 'select name from categories where id=%s' %(ans[7]) 
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        ans[7] = name[0][0] 
    
        # replace component_id by component name
        sql= 'select name from components where id=%s' %(ans[8]) 
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        ans[8] = name[0][0]

        # generate fixby
        fixby = ""
        sql = 'select product_id, version_id, phase_id from bug_fix_by_map where bug_id=%d' %(bugid)
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        product_id = name[0][0]
        version_id = name[0][1]
        phase_id = name[0][2]
        sql = 'select name from products where id=%d' %(product_id)
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        if (len(name) > 0):
            fixby += str(name[0][0])
        sql = 'select name from versions where id=%d' %(version_id)
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        if (len(name) > 0):
            fixby += " "
            fixby += str(name[0][0])
        sql = 'select name from phases where id=%d' %(phase_id)
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        if (len(name) > 0):
            fixby += " "
            fixby += str(name[0][0])
        ans.append(fixby)
        
        # generate thetext
        #    SQL: select group_concat(thetext) from longdescs group by bug_id limit %d,1' %(bugid)
        #       is too slow
        sql = 'set group_concat_max_len = 10240000'
        bz_cur.execute(sql)
        sql = 'select group_concat(thetext) from \
            (select thetext from longdescs where bug_id = %d) as myalias' %(bugid)
        bz_cur.execute(sql)
        name = bz_cur.fetchall()
        # add unicode to avoid json dumps error
        text = unicode(name[0][0], errors='replace')
        ans.append(text)          
        
        return ans

    def getFullText(self, bug):
        item = self.create_item(bug)
        fullText = item[9] +  item[11],
        #print doc
        return fullText[0]
    #def matchPR(self,fullText):
    #    return textMatcher.match(text)

    def testMatch(self, bug):
        text = self.getFullText(bug)
        print text
        ret = textMatcher.match(text,30,0.001)
        print ret

    def process(self):
        pr_kb_sql = 'select min(bug_id), kb_id from bug_kb_map group by kb_id'
        bz_cur.execute(pr_kb_sql)
        data = bz_cur.fetchall()
        pr_kb = []
        for d in data:
            m = {'pr':d[0], 'kb':d[1]}
            pr_kb.append(m)

        


        sdict = {}
        sqlkb = 'select kbnumber from symptom'
        cnx = mysql.connector.connect(user='root',password='vmware', database='unified')
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sqlkb)
        data = cursor.fetchall()
        for d in data:
            #osymps.append(d[0])
            sdict[str(d[0])] = 1
       #     print d
      
       # print sdict
        i = 0 
        m = 0
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
        threadnumber = 10

        while tid < threadnumber:
            thread.start_new_thread ( self.run, (r, tid, threadnumber,pr_kb, sdict) )
            tid = tid + 1


        #print r
    def run(self, r, tid, threadnumber, pr_kb, sdict):
        loop = 0
        for pk in pr_kb:
            #oprint ('thread %d ' % tid).join(r)
            if loop % threadnumber == tid:
                if sdict.has_key(pk['kb']):
                    mutex.acquire()
                    text = self.getFullText(pk['pr'])
                    mutex.release()
                    ret = textMatcher.match(text, 5, 0.1)
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
            loop = loop + 1
        print r







if __name__ == "__main__":
    import sys
    
    ev = EvaluateSearch()

    #print loader.create_item(1291688)
    #print loader.create_item(1335744)
    #print loader.create_item(1339158)
    ev.process()
    #ev.testMatch(1386722)
    while True:
        pass
