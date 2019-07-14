#!/usr/bin/python3
from PIL import Image 
import glob
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dirname', type=str, help='directory name')
parser.add_argument('--quality=', default=85, type=int, dest='quality', help='sets the quality of the reduced jpeg')
parser.add_argument('-o', action='store_true', help='optimizes the JPG and applies given quality setting')
parser.add_argument('-r', action='store_true', help='reduces the pixel size of the file by 0.325')

__DIRNAME__ = parser.parse_args().dirname
__QUALITY__ = parser.parse_args().quality
__OPTIMIZE__ = parser.parse_args().o
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

filenameSuffix = '_red.JPG'

# Get the entire path for the JPGs and RAWs
JPGs = [el for el in glob.glob(imageDirectory+'/*.JPG') if filenameSuffix not in el]
RAWs = [el for el in glob.glob(imageDirectory+'/*.NEF') if filenameSuffix not in el]

# loop through all of the JPG files to find the date that they were taken and sort by date into dictionary
dates=[] # need separate dates array to sort by dates later
fileDateTimes=[]
sortedPaths={}
for i,path in enumerate(JPGs):
    # gets the date and time 
    absoluteDateTime = datetime.strptime(GetDateTaken(path),'%Y:%m:%d %H:%M:%S')
    fileDateTimes.append(absoluteDateTime)

    # if the file has a date that isnt indexed yet, make a new dictionary entry and append the file path
    formattedDate = fileDateTimes[i].strftime('%d%m%Y')
    try:
        sortedPaths[formattedDate].append(path)
    except KeyError:
        sortedPaths[formattedDate] = []
        sortedPaths[formattedDate].append(path)

    # add the date object to the list of dates
    if absoluteDateTime.date() not in dates:
        dates.append(absoluteDateTime.date())

dates.sort()

# get user input to figure out the file prefix / description
filenamePrefix={}
for date in dates:
    # key is the formatted date string, the value is the file prefix / description
    filenamePrefix[date.strftime('%d%m%Y')] = input("Name for date "+str(date)+": ")

PrintDescription(sortedPaths,filenamePrefix)

# sorts all the dates by their filenumber
for formattedDate in sortedPaths.keys():
    SortFilenameByNumber(sortedPaths[formattedDate])

for formattedDate in sortedPaths.keys():

    # generate the path names
    rootPath = os.path.join(imageDirectory,'../'+formattedDate+'_'+filenamePrefix[formattedDate])
    cameraPath = rootPath+'/D610'
    rawPath = cameraPath+'/RAW'
    jpgPath = cameraPath+'/JPG'
    #videoPath = cameraPath+'/Videos'
    reducedPath = cameraPath+'/reduced/'

    # make folders
    os.mkdir(rootPath)
    os.mkdir(cameraPath)
    os.mkdir(rawPath)
    os.mkdir(jpgPath)
    #os.mkdir(videoPath)

    if __OPTIMIZE__:
        if not os.path.isdir(reducedPath):
            os.mkdir(reducedPath)

        for i,path in enumerate(sortedPaths[formattedDate]):

            img = Image.open(path)
            exif = im.info['exif']
            if __REDUCESIZE__:
                img = img.resize(tuple(int(el*0.325) for el in img.size),Image.ANTIALIAS)

            newPath = reducedPath+formattedDate+'_'+filenamePrefix[formattedDate]+'-'+str(i)+filenameSuffix
            newFilename = os.path.basename(newPath)

            img.save(newPath,quality=__QUALITY__,optimize=True,exif=exif)
            print("Reducing "+os.path.basename(path)+" | Saving as: "+newFilename)

    # move JPG and NEF files into JPG and RAW
    for path in sortedPaths[formattedDate]:
        os.rename(path,os.path.join(jpgPath,os.path.basename(path)))
        os.rename(path[:-3]+'NEF',os.path.join(rawPath,os.path.basename(path)[:-3]+'NEF'))

os.rmdir(imageDirectory)
