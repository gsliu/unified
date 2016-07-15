import sys
sys.path.append('.')
from lib.dbConn import getQueryBugzilla


class Bug:
    def __init__(self, bugId):
        self.bugId = bugId
        self.summary = None
        self.text = None
          

        #make query
        sql='select bug_id, creation_ts, bug_severity, priority, bug_status, assigned_to, reporter, category_id, component_id, short_desc from bugs where bug_id = %d' %(bugId)
        query = getQueryBugzilla()
        query.Query(sql)
        data = query.record
        if len(data) == 0:
            return

        # handle title encode
        self.summary = unicode(data[0]['short_desc'], errors='replace')

        # generate thetext
        #    SQL: select group_concat(thetext) from longdescs group by bug_id limit %d,1' %(bugid)
        #       is too slow
        sql = 'set group_concat_max_len = 10240000;'
        query = getQueryBugzilla()
        query.Query(sql)
      
        sql =  'select group_concat(thetext) as text from \
            (select thetext from longdescs where bug_id = %d) as myalias' %(bugId)
        query = getQueryBugzilla()
        query.Query(sql)
        data = query.record
        # add unicode to avoid json dumps error
        self.text = unicode(data[0]['text'], errors='replace')
    def getSummary(self):
        return self.summary
    
    def getText(self):
        return self.text

    def getBugId(self):
        return self.bugId

if __name__ == "__main__":
    bz = Bug(1291688)
    print bz.getSummary()
    print bz.getText()
