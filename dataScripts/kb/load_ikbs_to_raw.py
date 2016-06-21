#!/usr/bin/python 
import re
from datetime import datetime
from webpage import IKBPage
from os import listdir
from os.path import isfile, join

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class IKB_to_Raw_Loader:

##############################################################################
# RedHat Database structure:
#    KBid, URL, Symptoms, Resolution, Solution, Details, Purpose, Cause, Title
#    search fields name in es: 
#       merge fields "symptoms, resolution, solution, details, purpose, cause" into text
##############################################################################

    def __init__(self, sdir,ddir):
	self.kb_dir = sdir
        self.ddir = ddir
        self.regs = []
    #    self.create_index()      
        self.regs.append(re.compile(r'(<font[^>]+?Courier New*.+?<\/font>)'))
        self.regs.append(re.compile(r'(<span[^>].+?Courier New*.+?<\/span>)'))
        self.regs.append(re.compile(r'(<li[^>]+?Courier New*.+?<\/li>)'))
        self.regs.append(re.compile(r'(<code*.+?<\/code>)'))



    

    def save_item(self, page):
	text = page.get_title() + page.get_symptoms() + page.get_resolution() + page.get_solution() + page.get_cause() + page.get_purpose()  + page.get_details()

        f = open(self.ddir + page.get_id(), 'w')
        f.write(text)
        f.close()
      

    def remove_code(self,html):
        for r in regs:
            html = re.sub(r, "", html)
        return html

    def save_all(self):
        # iter all kbs
        for f in listdir(self.kb_dir):
            print "DEBUG: %s" %(f)
            file = join(self.kb_dir, f)
            if isfile(file):
                kb = IKBPage(file)
                tags = kb.get_tags()
                if 'Mandarin' in tags or 'Chinese' in tags or 'Japanese' in tags or 'Spanish' in tags or 'Portugues' in tags:
                    print 'ignore other langurage kb %s' % kb.get_id()
                    continue
                self.save_item(IKBPage(file))



if __name__ == "__main__":
    #import sys
    #print len(sys.argv)
    #if len(sys.argv) < 2:
    #    print "Please provide KB dirname"
    #    exit(0)
    
    #kb = IKBPage(file)
    #loader = IKB_to_ES_Loader(sys.argv[1])
    loader = IKB_to_Raw_Loader('/data/data/kbraw/data/', '/data/data/kbraw/raw/')
    

    loader.save_all()
