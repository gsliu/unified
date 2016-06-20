import os
import tarfile

g_after_extract_path='/data/data/bundle_after_extract/'
g_before_extract_path='/data/data/bundle_before_extract/'

class logExtractor:
    'Base class to extract log bundles of ESXi, VC or other product'
    def __init__(self, file):
        self.file = file
	print "Input bundle is %s"  %  file

class esxiLogExtractor(logExtractor):
    'for exi, *.tgz'
    def __init__(self, file):
        logExtractor.__init__(self, file)
    def extract(self):
        print 'Initing ESXi extractor...'
        split_filename = self.file.rsplit('.', 1)
        if "tgz" in split_filename:
            fn = self.file.decode('unicode-escape')
            tar = tarfile.open(fn, "r:gz")
            extracted = tar.next().name.split("/")[0]
          
            os.system("umask 000;tar zxvf " + self.file + ' -C ' + g_after_extract_path)

            ret = g_after_extract_path + extracted
            os.system("cd " + ret  + '/' + '; ./reconstruct.sh')
#            print "cd " + ret + '/' + '; ./reconstruct.sh'
            return ret

        else:
            print "The service bundle of ESXi host should by *.tgz, please check"

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
    bundle = "vmvspm0141.nm.nmfco.com-vmsupport-2016-02-23@15-05-08.tgz"
    bundle_full_path = g_before_extract_path + bundle
    esx = esxiLogExtractor(bundle_full_path)
    ret = esx.extract()
    print ret
