import sys
import argparse

sys.path.append('.')
from lib.symptomAnalyzerLog.scanLogClip import scanAll
from lib.symptomAnalyzerLog.buildSymptom import Builder
from lib.dataScript.loadKBToESLine import KBESLoader


def scanCode(args):
    #runset = sys.argv[1].split(';')
    #loaddir("/data/gengshengl/src/vsphere60p03/bora/vmx")  

    runset = []
    runset.append('/data/src/gengshengl/src/vsphere60p03/bora/')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/apps')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/lib')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/vmkernel')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/modules')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/devices')
    #runset.append('/data/src/gengshengl/src/vsphere60p03/bora/vim')
    #runset.append('/data/src/gengshengl/src/view623/mojo/')
    scanAll(runset)

def loadKB(args):
    loader = KBESLoader('/data/kbdata')
    #page = KBPage(2051492)
    #loader.indexItem(page)
    loader.indexAll()


def buildSymptom(args):
    builder = Builder()
    #builder.addLogTable('logclip_view')
    builder.addLogTable('logclip')
    builder.process()



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
build_parser = subparsers.add_parser('build', help='build symptom from log clips')
#delete_parser.add_argument('dirname', action='store', help='The directory to remove')
build_parser.set_defaults(func=buildSymptom) 


args = parser.parse_args()
args.func(args) 

