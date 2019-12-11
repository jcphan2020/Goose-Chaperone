from os import listdir
from os.path import isfile, join

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

mypath='./'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for s in onlyfiles:
    if (s!='whl_install.py'):
        print("Installing" + s)
        install(s)
#pscp bot_main.py debian@192.168.7.2:/home/debian/goose_chaperone/software
#pip3 download -d ./ pkg