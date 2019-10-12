import os
import PIL
from PIL import Image
from pathlib import Path

width = 480
height = 270

path='images'

files=[]

for root, dir, file in os.walk(path):
    for file in file:
        if '.jpg' in file:
            files.append(os.path.join(root, file))

for f in files:
    #print('..\\images_scaled\\'+f)
    file_name=os.path.splitext(f)[0]
    dir_name=os.path.dirname(f)
    print(file_name+' :: '+dir_name)
    raw = Image.open(f)
    wprcnt=(width/float(raw.size[0]))
    hsize=int((float(raw.size[1])*float(wprcnt)))
    raw = raw.resize((width, height), PIL.Image.ANTIALIAS)
    dirnm = '.\\images_scaled\\'+dir_name
    if (not os.path.exists(dirnm)):
        os.makedirs(dirnm)
    raw.save('.\\images_scaled\\'+file_name+'.jpg')