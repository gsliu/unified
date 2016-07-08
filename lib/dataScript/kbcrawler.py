#!/usr/bin/python

import sys
import urllib2

import redis

from threading import Thread

working_thread = []
r = redis.StrictRedis(host='localhost', port=6379, db=2)

class KBCrawler:
    def __init__(self, baseurl, number):
        self.baseurl = baseurl
	self.number = number
    def exist(self):
 	result = r.get(self.number)	
        return result	
    def getpage(self):
	try:
	    page = urllib2.urlopen(baseurl + str(self.number))
	    page_content = page.read()
	except:
	    return 'You are not authorized to access this article'
	return page_content
    def savefile(self):
	e = self.exist()

	internal =  'You are not authorized to access this article'
	notexist =  're sorry, but this Document is not currently available'
	if  e == None :
	    content = self.getpage()
	    if internal in content or notexist in content:
		r.set(self.number, 0) 	
		print 'invalid kb number ' + str(self.number)
	    else:
		with open('./data/' + str(self.number), 'w') as fid:
    		    fid.write(content)
		r.set(self.number, 1) 	
		print 'save kb ' + str(self.number)
	else :
	    print 'kb already accessed '  + str(self.number)

def savefilerange(low, high):
     for i in range(low, high):
         kc =  KBCrawler(baseurl, i)
         kc.savefile() 

if __name__ == "__main__":
    
    if len(sys.argv) < 4:
        print "start, end, max thread"
        exit(0)

    baseurl = 'http://kb.vmware.com/kb/'

    begin = int(sys.argv[1])
    end = int(sys.argv[2])
    low = begin;
    work_size = (end - begin) / int(sys.argv[3])
    high = min(low + work_size, end)

    while low < high:
        t = Thread(target = savefilerange, args = (low, high))
        t.start()
        low = high
        high = min(low + work_size, end)
        working_thread.append(t)
    for t in working_thread:
        t.join()

