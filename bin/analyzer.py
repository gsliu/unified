import sys
import argparse

sys.path.append('.')
from lib.logClip.scanString import scanAll
from lib.symptomAnalyzerLog.buildSymptom import BuildSymptom
from lib.symptomAnalyzerLog.initSymptom import InitSymptom
from lib.dataScript.loadKBToES import KBESLoader
from lib.logClip.scanFunction import ScanFunction


def scanCode(args):
    #runset = sys.argv[1].split(';')
    #loaddir("/data/gengshengl/src/vsphere60p03/bora/vmx")  

    runset = []
    runset.append('/data/srcdir/vsphere60p03/bora/')
    runset.append('/data/srcdir/vsphere60p03/vmkdrivers')
    runset.append('/data/srcdir/vsphere60p03/bora-vmsoft/')
    #runset.append('/data/srcdir/vsphere60p03/bora/')
    for srcdir in runset:
         sf = ScanFunction(srcdir)
         sf.process()
      
    scanAll(runset)

def loadKB(args):
    loader = KBESLoader('/data/kbdata')
    #page = KBPage(2051492)
    #loader.indexItem(page)
    loader.indexAll()


def buildSymptom(args):
    bs = BuildSymptom()
    bs.process()

def initSymptom(args):
    ini = InitSymptom()
    ini.addLogTable('logclip')
    ini.process()


parser = argparse.ArgumentParser()
#parser.add_argument('command')
#parser.add_argument()

subparsers = parser.add_subparsers( help='commands')

# scancode command
scan_parser = subparsers.add_parser('scan', help='Scan source code for log clips')
#scan_parser.add_argument('dirname', action='store', help='Directory to scan')
scan_parser.set_defaults(func=scanCode) 


# load kb to es command
load_parser = subparsers.add_parser('loadkb', help='load kb to es')
#create_parser.add_argument('dirname', action='store', help='New directory to create')
load_parser.set_defaults(func=loadKB) 


# build symptom command
build_parser = subparsers.add_parser('init', help='init symptom')
#delete_parser.add_argument('dirname', action='store', help='The directory to remove')
build_parser.set_defaults(func=initSymptom) 

# analyze log cluster
build_parser = subparsers.add_parser('build', help='analyze log cluster')
#delete_parser.add_argument('dirname', action='store', help='The directory to remove')
build_parser.set_defaults(func=buildSymptom) 



args = parser.parse_args()
args.func(args) 

