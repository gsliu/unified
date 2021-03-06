import os
import tarfile

g_after_extract_path='/data/data/bundle/task'
g_before_extract_path='/data/data/bundle/task'

class logExtractor:
    'Base class to extract log bundles of ESXi, VC or other product'
    def __init__(self, file):
        self.file = file
	print "Input bundle is %s"  %  file

class esxiLogExtractor(logExtractor):
    'for exi, *.tgz'
    def __init__(self, file):
        logExtractor.__init__(self, file)

    def extract(self, filename):
        print 'Initing ESXi extractor...'
        print filename
        split_filename = filename.rsplit('.', 1)
        if "tgz" in split_filename:
            fn = filename.decode('unicode-escape')
            print fn
            tar = tarfile.open(fn, "r")
            extracted = tar.next().name.split("/")[0]
            print "umask 000;tar zxvf " + filename + ' -C ' + self.file 
            os.system("umask 000;tar xvf " + filename + ' -C ' + self.file)
            ret = self.file + extracted
            print "ret = %s" % ret
            os.system("cd " + ret  + '/' + '; ./reconstruct.sh')
#            print "cd " + ret + '/' + '; ./reconstruct.sh'
            return ret

        else:
            print "The service bundle of ESXi host should by *.tgz, please check"

    def extractAllFiles(self):
        files = os.listdir(self.file)
        print files
        for f in files:
            if 'tgz' in f:
                print self.file + f
                self.extract(self.file + f)
            
        

class vcLogExtractor(logExtractor):
    'for vc, *.gz'
    def __init__(self):
        logExtractor.__init__(self, file)
    def extract(self):
        pass

class urlLogExtractor(logExtractor):
    'url type of service bundle, for example, http://xxxx/bugs/files/0/1/6/4/4/1/4/0/76/VMware-vCenter-support-2016-06-13@08-04-56.zip'
    'for vc, *.gz'
    def __init__(self):
        logExtractor.__init__(self, file)
    def extract(self):
        pass




if __name__ == '__main__':
    esx = esxiLogExtractor('/data/data/bundle/task1011/')
    ret = esx.extractAllFiles()
