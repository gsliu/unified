class logExtractor:
    'Base class to extract log bundles of ESXi, VC or other product'
    def __init__(self, file):
        self.file=file
        print 'Initing log extractor!'


class esxiLogExtractor(logExtractor):
    'for exi, *.tgz'
    def __init__(self):
        logExtractor.__init__(self, file)
    def extract(self):
        pass



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