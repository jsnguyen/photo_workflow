#!/usr/bin/python3
from PIL import Image 
import glob
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dirname', type=str, help='directory name')
parser.add_argument('--quality=', default=85, type=int, dest='quality', help='sets the quality of the reduced jpeg')
parser.add_argument('-r', action='store_true', help='reduces the pixel size of the file by 0.325')

__DIRNAME__ = parser.parse_args().dirname
__QUALITY__ = parser.parse_args().quality
__REDUCESIZE__ = parser.parse_args().r

def get_date_taken(path):
            return Image.open(path)._getexif()[36867]

imageDirectory = __DIRNAME__
saveDirectory  = os.path.join(__DIRNAME__,'reduced/')

filenameSuffix = '_red.JPG'
JPGs = [el for el in glob.glob(imageDirectory+'/*.JPG') if filenameSuffix not in el]
RAWs = [el for el in glob.glob(imageDirectory+'/*.NEF') if filenameSuffix not in el]
JPGsFilenames = [os.path.basename(el) for el in JPGs]
RAWsFilenames = [os.path.basename(el) for el in RAWs]

# representative file of the set
repFile =  JPGs[0]

dates=[]
fileDateTimes=[]
sortedPaths={}
for i,path in enumerate(JPGs):
    absoluteDateTime = datetime.strptime(get_date_taken(path),'%Y:%m:%d %H:%M:%S')
    fileDateTimes.append(absoluteDateTime)
    formattedDate = fileDateTimes[i].strftime('%d%m%Y')
    if absoluteDateTime.date() not in dates:
        dates.append(absoluteDateTime.date())

    try:
        sortedPaths[formattedDate].append(path)
    except KeyError:
        sortedPaths[formattedDate] = []
        sortedPaths[formattedDate].append(path)

dates.sort()
filenamePrefix={}
for date in dates:
    filenamePrefix[date.strftime('%d%m%Y')] = input("Name for date "+str(date)+": ")

print(filenamePrefix)
print(sortedPaths.keys())
print([len(sortedPaths[key]) for key in sortedPaths.keys()])
for key in sortedPaths.keys():
    sortedPaths[key].sort(key=lambda f: int(''.join(filter(str.isdigit,os.path.basename(f)))))

if not os.path.isdir(saveDirectory):
    os.mkdir(saveDirectory)

for i,formattedDate in enumerate(sortedPaths.keys()):
    for j,path in enumerate(sortedPaths[formattedDate]):

        img = Image.open(path)
        if __REDUCESIZE__:
            img = img.resize(tuple(int(el*0.325) for el in img.size),Image.ANTIALIAS)

        newPath = saveDirectory+formattedDate+'_'+filenamePrefix[formattedDate]+'-'+str(j)+filenameSuffix
        newFilename = os.path.basename(newPath)

        img.save(newPath,quality=__QUALITY__,optimize=True)
        print("Reducing "+os.path.basename(path)+" | Saving as: "+newFilename)
