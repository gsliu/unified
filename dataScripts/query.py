#!/usr/bin/python

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)


with open('functions') as fp:
    for line in fp:
	line = line.strip(' \t\n\r')
	result = r.get(line)
       	print line + ' = ' + result 

