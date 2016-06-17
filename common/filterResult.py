import re
import os
import sys
import itertools

sys.path.append('..')

from dataScripts.kb.webpage import IKBPage


#return value
# kbtitle
# kburl
# kbtext
# star
def filterResult(ret, size, minscore):
    #sort and trim ret by size 
    ret = sorted(ret, key=lambda k: k['score'], reverse=True)  
    ret = ret[:size] 

    #drop match below minscore 
    newret = [] 
    for r in ret: 
        if r['score'] > minscore: 
            newret.append(r) 
    

    newret = rank(newret)
 
    jret = []
    for r in newret:
        page = IKBPage('/data/data/kbraw/data/%s' %r['kbnumber'])
        j = dict()
        j['url'] = 'http://kb.vmware.com/%d' % r['kbnumber']
        j['title'] = page.get_title()
        j['text'] = textmatched(r,page)
        j['rank'] = r['rank']
        jret.append(j)
        #print j

    return jret

def textmatched(r, page):
    text = '...'
    kbtext = page.get_text()
    #print kbtext
    
    for log in r['logs']:
       if log['matched']:
           
           print log['log']
           start = kbtext.find(log['log'])
           if start > 0:

               if start < 30:
                   start = 0
               else:
                   start = start - 30
	       end = start + 60 + len(log['log'])
               text = text + kbtext[start:end]
               text = re.sub(r'%s' % log['log'], '<b>%s</b> '%  log['log'], text)
           if len(text) > 200:
               break
           
           
    text = text + '...'
    return text

def rank(ret):
    scores = []
    for r in ret:
        scores.append(r['score'])

    stars = star(scores)

 
    for r, s in zip(ret, stars):
        r['rank'] = s
    return ret
    

def star(scores):
    rank = []
    for s in scores:
        rank.append(5)
    return rank
     
