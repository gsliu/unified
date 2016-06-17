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
    

   rank = star(scores)
    
    jret = []
    for r in newret:
        page = IKBPage(r['kbnumber']
        j = {}
        j['url'] = 'http://kb.vmware.com/ %d' % r['kbnumber']
        j['title'] = page.get_title()
        j['text'] = textmatched(r,page)
        j['rank'] = r['rank']
        jret.append(j)
        #print j

    return jret

def textmatched(r, page):
    text = '...'
    kbtext = page.get_text()
    
    for log in r['log']:
       if log['matched']:
           p = re.compile(r'%s', log['log'])
           m = r.finditer(kbtext)
           if m:
               startpos = m.start()
               if start < 30:
                   start = 0
	       end = start + 60 + len(log['log'])
               text = text + logtext[start:end]
               text = re.sub(r"%s", "<b>%s</b>" % (log['log'], log['log']), text)
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
     
