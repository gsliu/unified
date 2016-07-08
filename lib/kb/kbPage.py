#!/usr/bin/python

import lxml.html    # python-lxml
import urlparse
import re
import os
from HTMLParser import HTMLParser
from logCheckKBHtml import MLStripper
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
        #CHANGES Apr 17 2011 START
        #patterns = []
        #for p in str_patterns:
        #    patterns.append(re.compile(p))
        #CHANGES Apr 17 2011 E N D
        ##
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


class KBPage( WebPage ):

    def __init__(self, kbnumber, datadir='/data/kbdata'):
	self.kbnumber = kbnumber
	filename = os.path.join(datadir, str(kbnumber))
        url = "http://kb.vmware.com/kb/" + str(self.kbnumber)
        with open(filename, 'r') as f:
            html = f.read()
        WebPage.__init__(self, url, html)
        self.resolution_class_name = "cc_Resolution"
        self.solution_class_name = "cc_Solution"
        self.details_class_name = "cc_Details"
        self.purpose_class_name = "cc_Purpose"
        self.cause_class_name = "cc_Cause"
        self.symptoms_class_name = "cc_Symptoms"
        self.tags_class_name = "cc_Tags"
        self.body_els = self.doc.findall('./body/')
        #print self.body_els
        
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

    def getLog(self):
        return self.log

    def stripTags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def getText(self):
        ret = self.getSymptoms() + self.getCause() + self.getPurpose() + self.getDetails() + self.getSolution() + self.getResolution()
        ret = re.sub(r'[<>]', "", ret)
        return ret


 
    def getFullText(self):
        return self.getTitle() + self.getSymptoms() + self.getCause() + self.getPurpose() + self.getDetails() + self.getSolution() + self.getResolution()
 
    def getIndexText(self):
        text =  self.getTitle() + self.getSymptoms() + self.getCause() + self.getPurpose() + self.getDetails() + self.getSolution() + self.getResolution()
        text = re.sub(r'[\n]+', '#u#u', text)
        return text


if __name__ == "__main__":
    kb = KBPage(2034627)
    kb = KBPage(2119642)
    kb = KBPage(2097684)
    print kb.getKbnumber()
    print kb.getFullText()
