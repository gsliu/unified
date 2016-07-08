#!/usr/bin/python

import os
import html2text
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

class KBText :

    def __init__(self, kbnumber, datadir='/data/kbdata'):
	self.kbnumber = kbnumber
	filename = os.path.join(datadir, str(kbnumber))
        url = "http://kb.vmware.com/kb/" + str(self.kbnumber)
        with open(filename, 'r') as f:
            html = f.read()
	    self.text = html2text.html2text(html)

    def getText(self):
        return self.text

if __name__ == "__main__":
    kb = KBText(2034627)
    print kb.getText()
