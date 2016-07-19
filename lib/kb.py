#!/usr/bin/python

import lxml.html    # python-lxml
import urlparse
import re
import os
from HTMLParser import HTMLParser
import html2text

class WebPage:
    
    ###########################################
    #   WEBPAGE CONSTRUCTOR
    ###########################################
    def __init__(self, url, html):
        self.url = url
        self.html = html
        self.doc = lxml.html.fromstring(self.html)
        #print self.doc
        self.links = {}

    #######################################
    # parsing links from html page
    #######################################
    def parse_links(self):
        for elem, attr, link, pos in self.doc.iterlinks():
            absolute = urlparse.urljoin(self.url, link.strip())
            #print elem.tag ,attr, absolute, pos
            if elem.tag in self.links:
                self.links[elem.tag].append(absolute)
            else:
                self.links[elem.tag] = [absolute]
        return self.links

    # filter links
    def filter_links(self,tags=[],patterns=[]):
        filterlinks = []
        if len(tags)>0:
            for tag in tags:
                for link in self.links[tag]:
                    if len(patterns) == 0:
                        pass
                        #filterlinks.append(link)
                    else:
                        for pattern in patterns:
                            if pattern.match(link)!=None:
                                filterlinks.append(link)
                                continue
        else:
            for k,v in self.links.items():
                for link in v:
                    if len(patterns) == 0:
                        pass
                        #filterlinks.append(link)
                    else:
                        for pattern in patterns:
                            if pattern.match(link)!=None:
                                filterlinks.append(link)
                                continue

        return list(set(filterlinks))

        return filterlinks    


class KB( WebPage ):

    def __init__(self, kbnumber, datadir='/data/kbdata'):
	self.kbnumber = kbnumber
	filename = os.path.join(datadir, str(kbnumber))
        self.url = "http://kb.vmware.com/kb/" + str(self.kbnumber)
        
        with open(filename, 'r') as f:
            self.html = f.read()
        WebPage.__init__(self, self.url, self.html)
        self.resolution_class_name = "cc_Resolution"
        self.solution_class_name = "cc_Solution"
        self.details_class_name = "cc_Details"
        self.purpose_class_name = "cc_Purpose"
        self.cause_class_name = "cc_Cause"
        self.symptoms_class_name = "cc_Symptoms"
        self.tags_class_name = "cc_Tags"
        self.body_els = self.doc.findall('./body/')

        # for log extraction
        self.regs = []
        self.regs.append(re.compile(r'(<font[^>]+?courier new*.+?<\/font>)'))
        self.regs.append(re.compile(r'(<span[^>].+?courier new*.+?<\/span>)'))
        self.regs.append(re.compile(r'(<li[^>]+?courier new*.+?<\/li>)'))
        self.regs.append(re.compile(r'(<code*.+?<\/code>)'))
        self.regs.append(re.compile(r'(<tt*.+?<\/tt>)'))

        
        if len(self.body_els) > 1:
            pass
            #print "Warning: more than one body in html"
 
    def getTitle(self):
        e = self.doc.findall('./head/title')
        if len(e) > 1:
            pass
            #print "Warning: more than one title in html"
        if len(e) == 0:
            return ""
        else:
            return e[0].text_content() + '\n'
        
    def getKbnumber(self):
        return self.kbnumber 

    def getEle(self, name):
        for ele in self.body_els:
            e = ele.find_class(name)
            if len(e) > 1:
		pass
                #print "Warning: more than one %s in html" %(name)
            elif len(e) == 0:
                continue
            else:
                html = lxml.html.tostring(e[0])
                html = re.sub(r'<img[^>]*>', '', html)
                text = html2text.html2text(html)
                #print 'trimming.........'
                #text = re.sub(r'base64,.*\n', '', text)
                return text + '\n'
        return  ""

    def getSymptoms(self):
        return self.getEle(self.symptoms_class_name)
    
    def getCause(self):
        return self.getEle(self.cause_class_name)

    def getPurpose(self):
        return self.getEle(self.purpose_class_name)
    
    def getDetails(self):
        return self.getEle(self.details_class_name)

    def getSolution(self):
        return self.getEle(self.solution_class_name)

    def getResolution(self):
        return self.getEle(self.resolution_class_name)
    
    def getTags(self):
        return self.getEle(self.tags_class_name)

    def getUrl(self):
        return self.url    


    def getText(self):
        ret = self.getSymptoms() + self.getCause() + self.getPurpose() + self.getDetails() + self.getSolution() + self.getResolution()
        ret = re.sub(r'[<>]', "", ret)
        return ret


 
    def getFullText(self):
        return self.getTitle() + self.getSymptoms() + self.getCause() + self.getPurpose() + self.getDetails() + self.getSolution() + self.getResolution()
 
    def getLog(self):
        kblog = ""
        text = self.html
        #print text
        for reg in self.regs:
            m1 = reg.findall(text)
            #print reg 
            if m1:
                for string in m1:
                    kblog = kblog +  html2text.html2text(string)
        return kblog

    def getLogCluster(self):
        cluster = []
        n = 0
        text = self.html
        for reg in self.regs:
            m1 = reg.findall(text)
            if m1:
                for string in m1:
                    cluster.append(html2text.html2text(string))
        return cluster




if __name__ == "__main__":
    kb = KB(2034627)
    kb = KB(2119642)
    kb = KB(2097684)
    kb = KB(2135810)
    #print kb.getKbnumber()
    #print kb.getFullText()
    #print kb.getDetails()
    print kb.getLog()
    print kb.getLogCluster()
