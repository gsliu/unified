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
        j['url'] = 'http://kb.vmware.com/kb/%d' % r['kbnumber']
        j['kbnumber'] = r['kbnumber']
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
               try:
                   text = re.sub(r'%s' % log['log'], '<b>%s</b> '%  log['log'], text)
               except:
                   pass

           if len(text) > 300:
               break
           if len(text) < 300:
              text = kbtext[0:300] + text
           
           
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
    

def star(listofscore):
    star = []
    lessthan_ave = []
    ave_number = sum(listofscore)/len(listofscore)
    max_number = max(listofscore)
    min_number = min(listofscore)
    for i in range(len(listofscore)):
        if (listofscore[i] <= ave_number):
            lessthan_ave.append(listofscore[i])
    max_less_ave = max(lessthan_ave)
    for i in range(len(listofscore)):
        if (listofscore[i] > ave_number):
            if(listofscore[i] == max_number):
                star.append(5)
            else:
                hdelta = listofscore[i] - ave_number
                star_hscore = 3-hdelta%3 + 2
                star.append(round(star_hscore))
        else:
            if(listofscore[i] == max_less_ave):
                star.append(3)
            elif(listofscore[i] == min_number):
                star.append(1)
            else:
                ldelta = ave_number - listofscore[i]
                star_lscore = 3 - ldelta%3
                star_int = round(star_lscore)
                star.append(star_int)
    return star
     
