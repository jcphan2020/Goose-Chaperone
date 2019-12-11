from os import listdir
from os.path import isfile, join

import subprocess
import sys

def copy(file):
    subprocess.check_call([sys.executable, "pscp", file, "debian@192.168.7.2:/home/debian/goose_chaperone/software"])

mypath='./'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for s in onlyfiles:
    if (s!='whl_copy.py'):
        print("Copying" + s)
        install(s)
#pscp bot_main.py debian@192.168.7.2:/home/debian/goose_chaperone/software