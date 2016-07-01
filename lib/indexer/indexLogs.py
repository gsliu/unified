import sys
import os
import pyes
import json


class IndexLogs(object):
    def __init__(self, logDir, indexname):
        conn = pyes.ES('http://unified.eng.vmware.com:9200')
        
        #mapping = {
        #u'parsedtext': {
        #    'boost': 1.0,
        #    'index': 'analyzed',
        #    'store': 'yes',
        #    'type': u'string',
        #    "term_vector": "with_positions_offsets"},
        #u'name': {
        #    'boost': 1.0,
        #    'index': 'analyzed',
        #    'store': 'yes',
        #    'type': u'string',
        #    "term_vector": "with_positions_offsets"},
        #u'title': {
        #    'boost': 1.0,
        #    'index': 'analyzed',
        #    'store': 'yes',
        #    'type': u'string',
        #    "term_vector": "with_positions_offsets"},
        #u'pos': {
        #    'store': 'yes',
        #    'type': u'integer'},
        #u'doubles': {
        #    'store': 'yes',
        #    'type': u'double'},
        #u'uuid': {
        #    'boost': 1.0,
        #    'index': 'not_analyzed',
        #    'store': 'yes',
        #    'type': u'string'}}

        conn.indices.delete_index_if_exists(indexname)
        conn.indices.create_index(indexname)
        #conn.indices.put_mapping("test-type", {'properties': mapping}, ["test-pindex"])
        #conn.index({"name": "Joe Tester", "parsedtext": "Joe Testere nice guy", "uuid": "11111", "position": 1,
        #    "doubles": [1.0, 2.0, 3.0]}, indexname, "test-type", 1)

        for logfile in self.findLogFiles(logDir):
            if os.path.isfile(logfile):
                j = self.toBeJason(logfile)
                conn.index(j, indexname, "test-type")  # Index a typed JSON document into a specific index and make it searchable.
            else:
                print "There is not file in %s." %(logDir)

        if os.path.isfile(self.findCommentFile(logDir)):
            j = self.toBeJason(self.findCommentFile(logDir)) 
            conn.index(j, indexname, "test-type")
        else:
            print "There is no comment text file."


    def findLogFiles(self, logDir):
        logFiles = []

        for root, subFolders, files in os.walk(logDir):
            for file in files:
                if file[-4:] == '.log':
                    filePath = root + '/' + file
                    logFiles.append(filePath)
        #print logFiles
        return logFiles

    def findCommentFile(self, logDir):
        fileList = os.listdir(logDir)
        commentFile = ''

        for line in fileList:
            if line == 'text':
                commentFile = os.path.join(logDir, line)
        #print commentFile
        return commentFile


    def toBeJason(self, logFile):   #logFile is file name with full path
        #fp = open(os.path.join(logDir, logFile))
        fp = open(logFile)
        logContent = fp.read()

        data = dict({'logFileName':logFile, 'logs':logContent})
        encodedjson = json.dumps(data)
        #print encodedjson

        file.close(fp)
        return encodedjson


if __name__ == '__main__':
    inde = IndexLogs('/data/', "tast-indexname")
    #inde.findLogFiles('/data/Min/unified/common/logs')


