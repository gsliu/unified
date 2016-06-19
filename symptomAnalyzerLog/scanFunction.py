#!/usr/bin/python

from scanLogClip import ScanCodeClip

class FunctionMysql:
    def __init__(self, function):
        print function
        self.function = function
        self.s = ScanCodeClip(' ', 'function_name') 

    def process(self):
        with open(self.function) as fp:
            for line in fp:
                print line
	        line = line.strip(' \t\n\r')
                self.s.process(line)


if __name__ == '__main__':
    f = FunctionMysql('/data/data/dict/functions')
    f.process()

