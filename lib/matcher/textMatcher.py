import sys
import os
import re


sys.path.append('.')
from lib.matcher.filterResult import Result
from lib.matcher.filterResult import SymptomResult
from lib.matcher.filterResult import ClusterResult
from lib.matcher.lineDict import LineDict

from lib.matcher.matcher import Matcher
from lib.symptomHits import SymptomHits

sh = SymptomHits()



class TextMatcher(Matcher):
                 
        

    #core matchting algorithm
    # totalscore = 0
    # Foreach cluster in Symptom
    # clusterscore = 0
    # foreach logclip  in cluster
    #     if match:
    #         create log interval
    #         Merge cluster interval
    #         clusterscore += logscore
    # totalscore += clusterscore * N ( N is the number of matched log in cluster)  

    def match(self, text, size=10, minscore=0.5):
        text = text.lower()
        ld = LineDict(text)
        result = Result(maxSize = size, minscore=minscore)
        for s in self.symptoms:
            symptomResult = SymptomResult(s.getKbnumber())

            for cluster in s.getCluster():
                clusterResult = ClusterResult()
                if cluster['cluster'] == -1:
                    continue
                for log in cluster['logs']:
                    lines = ld.getLines(log['log'])
                    if lines > 0: 
                        matchItem = {'pos':lines, 'log':log}
                        clusterResult.mergeClusterInterval(matchItem)

                cluster = clusterResult.highestScoreCluster()
                if cluster:
                    symptomResult.addCluster(cluster)
        
            if len(symptomResult.getCluster()) > 0:
                result.addSymptomResult(symptomResult)
        return result.getResult()
      

    #core matchting algorithm
    def match1(self, text, size=10, minscore=0.5):
        ret = []
        for s in self.symptoms:
            
            score = 0.0 
            mln = 0
            logs = []
            for log in s.getLogs():
                if log['log'] in text:
                    log['matched'] = 1
		    score = score + log['score']
                    mln = mln + 1
                else:
                    log['matched'] = 0
                
                logs.append(log)

            if mln > 0:
                ret.append({'kbnumber':s.getKbnumber(), 'score':score, 'matchedlog':mln, 'logs':logs})

        #update hits
        fret = filterResult(ret, size, minscore)
        for r in fret:
            sh.hit(r['kbnumber'])


        print fret
        return fret
       
                
                    
            


if __name__ == '__main__':
    m = TextMatcher(0)
    #sym = m.getSymptoms()
    ret = m.match("Workflow 'AppServiceDisposeVM' failed with the following exception: An error occurred while executing the workflow. For more details, see the inner exception. Inner Exception: Error executing vCenter Orchestrator workflow: com.vmware.o11n.plugins.nsx.error.VsmException: VSM response error (841): virtualwire-xxx resources are still in use..\nAn error occurred while executing the workflow. For more details, see the inner exception. Error executing vCenter Orchestrator workflow: com.vmware.o11n.plugins.nsx.error.VsmException: VSM response error (841): virtualwire-xxx resources are still in use.")
    print ret
    ret = m.match("YYYY-MM-DDT18:05:57.424Z [3DF03B90 info 'Hostsvc.HaHost'] vmxSwapEnabled = true vmmOvhd.anonymous: 22964 vmmOvhd.paged: 63957 vmmOvhd.nonpaged: 13771")
    print ret
    ret = m.match("YYYY-MM-DDT18:05:57.433Z [3DF03B90 info 'Vcsvc.VMotionSrc (1388772268136447)'] ResolveCb: VMX reports needsUnregister = false for migrateType MIGRATE_TYPE_VMOTION")
    print ret
    ret = m.match("YYYY-MM-DDT18:04:27.748Z [4FA40B70 warning 'Vcsvc.VMotionDst (1388772268136447)' opID=57C757C9-000004C9-9c-75-89 user=vpxuser] Bind: Failed to initialize VMotionWorker")
    print ret
    #f = open('log')
    #ret = m.match(f.read())
    #for r in ret:
     #   print "%s, %2.8f" % (r['kbnumber'], r['score'])
    #print ret
