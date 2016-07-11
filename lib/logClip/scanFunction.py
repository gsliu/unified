import sys
import commands

sys.path.append('.')

from lib.logClip.logClip import LogClip

class ScanFunction:
    def __init__(self, srcdir):
        self.lc = LogClip()
	self.srcdir = srcdir

    def process(self):
        output = commands.getstatusoutput('cd %s;cscope -R -L -0 ".*" | awk -F \' \' \'{print $2}\' | sort | uniq' % self.srcdir)
        for f in output[1].split('\n'):
            self.lc.saveLog(f)
             


if __name__ == '__main__':
    sf = ScanFunction('/data/src/gengshengl/src/vsphere60p03/bora/vmx/main')
    sf.process()

