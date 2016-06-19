from rake import rake
import operator
import sys

sys.path.append('..')

from dataScripts.kb.webpage import IKBPage






page = IKBPage('/data/data/kbraw/data/1021836')
text = page.get_fulltext()
keywords = rake.rake(text)
print "Keywords:", keywords
