#!/usr/bin/python3
from PIL import Image 
import glob
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('date', type=str, help='sets the filename prefix')
parser.add_argument('prefix', type=str, help='sets the filename prefix')
parser.add_argument('dirname', type=str, help='directory name')
parser.add_argument('--quality=', default=85, type=int, dest='quality', help='sets the quality of the reduced jpeg')
parser.add_argument('-r', action='store_true', help='reduces the pixel size of the file by 0.325')

__DIRNAME__ = parser.parse_args().dirname
__QUALITY__ = parser.parse_args().quality
__PREFIX__ = parser.parse_args().prefix
__DATE__ = parser.parse_args().date
__REDUCESIZE__ = parser.parse_args().r

def GetDateTaken(path):
    return Image.open(path)._getexif()[36867]

def PrintDescription(desc,prefix):
    print("--- DDMMYYYY filePrefix nFiles ---") 
    for key in prefix.keys():
        print('-->',key,prefix[key],len(desc[key]))

def SortFilenameByNumber(arr):
    arr.sort(key=lambda f: int(''.join(filter(str.isdigit,os.path.basename(f)))))


imageDirectory = __DIRNAME__
saveDirectory  = os.path.join(__DIRNAME__,'reduced/')
filenamePrefix = __PREFIX__

filenameSuffix = '_red.JPG'

# Get the entire path for the JPGs and RAWs
JPGs = [el for el in glob.glob(imageDirectory+'/*.JPG') if filenameSuffix not in el]
SortFilenameByNumber(JPGs)

for path in JPGs:

    if not os.path.isdir(saveDirectory):
        os.mkdir(saveDirectory)

    for i,path in enumerate(JPGs):

        img = Image.open(path)
        if __REDUCESIZE__:
            img = img.resize(tuple(int(el*0.325) for el in img.size),Image.ANTIALIAS)

        newPath = saveDirectory+__DATE__+'_'+filenamePrefix+'-'+str(i)+filenameSuffix
        newFilename = os.path.basename(newPath)

        img.save(newPath,quality=__QUALITY__,optimize=True)
        print("Reducing "+os.path.basename(path)+" | Saving as: "+newFilename)


os.rmdir(imageDirectory)
