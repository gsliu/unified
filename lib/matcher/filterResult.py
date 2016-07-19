import re
import os
import sys
import itertools


from lib.kb import KB


class Interval:
    def __init__(self, s=0, e=0, logs=[]):
        self.start = s
        self.end = e
        self.logs = logs

    def toDict(self):
        return {'start':self.start, 'end':self.end, 'logs':self.logs}

class ClusterResult:
    def __init__(self, offset= 100):
        self.logRes = []
        self.offset = offset
  
    def mergeLogs(self, logs1, logs2):
        ld = {}
        for log in logs1:
            ld[log['log']] = 1
        for log in logs2:
            if not ld.has_key(log['log']):
                logs1.append(log)
      
        return logs1 

    def mergeInterval(self):
        if not self.logRes:
            return 

        self.logRes.sort(key=lambda x: x.start)

        result = [self.logRes[0]]
        for i in xrange(1, len(self.logRes)):
            prev, current = result[-1], self.logRes[i]
            if current.start <= prev.end: 
                prev.end = max(prev.end, current.end)
                prev.logs = self.mergeLogs(prev.logs, current.logs)
            else:
                result.append(current)
        return result

    def mergeClusterInterval(self, matchItem):
        for pos in matchItem['pos']:
            flag = True
            for interval in self.logRes:
                if pos > interval.start - self.offset and pos < interval.end + self.offset:
                   interval.logs.append(matchItem['log'])
                   interval.start = min(interval.start, pos)
                   interval = max(interval.end, pos)
                   self.mergeInterval()
                   flag = False

            if len(self.logRes) == 0 or flag:
                self.logRes.append(Interval(pos, pos, [matchItem['log']]))

     
    def highestScoreCluster(self):
        maxscore = -1.0;
        ret = None
        for interval in self.logRes:
            ts = 0
            for log in interval.logs:
                ts = ts + log['score']
            if ts > maxscore:
                maxscore = ts
                ret = interval
        return ret


class SymptomResult:
    def __init__(self, kbnumber):
        self.clusterRes = []
        self.kbnumber = kbnumber
          
    def getScore(self):
        score = 0
        for interval in self.clusterRes:
            for log in interval.logs:
                score = score + log['score']
        return score

    def addCluster(self, cluster):
        self.clusterRes.append(cluster)

    def getCluster(self):
        return self.clusterRes

    def getKbnumber(self):
        return self.kbnumber

    def textmatched(self, logs, page):
        text = '...'
        kbtext = page.getText()
        #print kbtext
    
        for log in logs:
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
    def getClusterDict(self):
        res = []
        for interval in self.clusterRes:
            res.append(interval.toDict())
        return res

    def getResult(self):
        page = KB(self.getKbnumber())
        logs = []
        for interval in self.clusterRes:
            logs = interval.logs + logs

        ret = {
            'kbnumber':self.kbnumber, 
            'url':page.getUrl(),
            'title': page.getTitle(),
            'text': self.textmatched(logs,page),
            'score': self.getScore(), 
            'clusters':self.getClusterDict(),
        }
        return ret


class Result:
    def __init__(self, maxSize = 30, minscore = 0.005):
        self.symptomRes = []
        self.minscore = minscore
        self.maxSize = maxSize
 
    def addSymptomResult(self,symptomResult):
        #if symptomResult.getScore() < self.minscore:
        #    return
        #print self.symptomRes
        self.symptomRes.append(symptomResult)
        if len(self.symptomRes) > self.maxSize:
            self.symptomRes.sort(key=lambda x: x.getScore(), reverse=True) 
            self.symptomRes = self.symptomRes[0:self.maxSize - 1]

    def getSymptomResult(self):
        return self.symptomRes

    def rank(self, ret):
        scores = []
        for r in ret:
            scores.append(r['score'])

        stars = self.star(scores)
 
        for r, s in zip(ret, stars):
            r['rank'] = s
        return ret
    

    def star(self, listofscore):
        if len(listofscore) == 0:
            return []
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
 
    def getResult(self):
        res = []
        for symptomResult in self.symptomRes:
            res.append(symptomResult.getResult())
        res = self.rank(res)
        return res

        #return  clusterRes


