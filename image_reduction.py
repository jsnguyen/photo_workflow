#!/usr/bin/python3
from PIL import Image 
import glob
import os
from datetime import datetime

def get_date_taken(path):
            return Image.open(path)._getexif()[36867]

imageDirectory = "/home/jsnguyen/110ND610/"
saveDirectory  = "/home/jsnguyen/110ND610/reduced/"

filenameSuffix = '_red.JPG'
JPGs = [el for el in glob.glob(imageDirectory+'*.JPG') if filenameSuffix not in el]
RAWs = [el for el in glob.glob(imageDirectory+'*.NEF') if filenameSuffix not in el]
JPGsFilenames = [os.path.basename(el) for el in JPGs]
RAWsFilenames = [os.path.basename(el) for el in RAWs]

# representative file of the set
repFile =  JPGs[0]

filenamePrefix = "DesolationForest"

dates=[]
fileDateTimes=[]
for i,path in enumerate(JPGs):
    print(path)
    absoluteDateTime = datetime.strptime(get_date_taken(path),'%Y:%m:%d %H:%M:%S')
    fileDateTimes.append(absoluteDateTime)
    if(absoluteDateTime.date() not in dates):
        dates.append(absoluteDateTime.date())

if not os.path.isdir(saveDirectory):
    os.mkdir(saveDirectory)

for i,path in enumerate(JPGs):
    formattedDate = fileDateTimes[i].strftime('%d%m%Y')

    img = Image.open(path)
    img = img.resize(tuple(int(el*0.325) for el in img.size),Image.ANTIALIAS)

    newPath = saveDirectory+formattedDate+'_'+filenamePrefix+'-'+str(i)+filenameSuffix
    newFilename = os.path.basename(newPath)

    img.save(newPath,quality=85,optimize=True)
    print("Reducing "+JPGsFilenames[i]+" | Saving as: "+newFilename)
