import os
import shutil
import glob
import pathlib
from datetime import datetime
import argparse

from PIL import Image

##########################################################################
# Description:
# Automatically import files and sort them into JPG, RAW, and video files.
# Needs input to pick the date, set the title, and set camera name if it
# cannot be determined from the image files.

# Usage:
# python3 ./pwimport.py <search_dir>
##########################################################################

# make the directory in a protected way, fails if directory cant be made
# tries to make the parent directories if not available
# also doesn't fail if directory already exists
def make_dir_protected(ddir):
    try:
        pathlib.Path(ddir).mkdir(parents=True, exist_ok=True)
    except:
        raise Exception('Creation of the directory {} failed'.format(ddir))
    else:
        print('Successfully created the directory {} '.format(ddir))

# recursive search in directory of all files in list of extensions
# gets both the path and the date of creation as a datetime
# returns a dictionary where the keys are the dates and values are the files
def get_all_files_with_ext(search_dir, exts):
    files = {}
    datetimes = []
    paths = []
    for ext in exts:
        for path in pathlib.Path(search_dir).rglob('*.'+ext):
            ctime = os.path.getmtime(path.as_posix()) # gets the time in unix time (seconds)
            file_datetime = datetime.fromtimestamp(ctime)

            datetimes.append(file_datetime)
            paths.append(path)

            date = file_datetime.date()

            try:
                files[date].append(path)
            except KeyError:
                files[date] = []
                files[date].append(path)

    return files

# copy files using copy2 to preserve as much metadata as possible
def copy_files(filenames, data_dir):
    for el in filenames:
        print('Copying {} to {}'.format(el,data_dir))
        shutil.copy2(el,data_dir)

# make sure that the source search directory is a mounted volume
# check that it's some form of external storage like an SD card
# *** NOT IDIOT PROOF! ***
# idk how to make it so that it cant search the entire hdd
def is_valid_search_dir(directory):
    is_good = False
    if pathlib.Path('/Volumes') in directory.parents:
        if os.path.ismount(directory):
            is_good = True

    return is_good

# naive way of trying to get the camera name from the exif data
# probably likely to fail, but good enough for now
def get_camera_name(image_filename):
    image = Image.open(image_filename)
    exif = image.getexif()
    camera_name = exif[272]
    return camera_name

# main routine for copying 
def pimport(args):
    search_dir = pathlib.Path(args.search_dir)

    if not os.path.isdir(search_dir):
        print('[ERROR]: Directory does not exist!')
        return

    # should be something like /Volumes/<dir>
    # also should be valid mount point
    if not args.n:
        if not is_valid_search_dir(search_dir):
            print('[ERROR]: Invalid search directory!')
            return
    
    # search for files in directory by extension
    # sort jpg, raw and video files separately
    jpg_ext = ['JPG']
    jpg_files = get_all_files_with_ext(search_dir, jpg_ext)

    raw_ext = ['NEF', 'CR3', 'RAF']
    raw_files = get_all_files_with_ext(search_dir, raw_ext)

    video_ext = ['MP4', 'MOV']
    video_files = get_all_files_with_ext(search_dir, video_ext)

    # attempts to get camera name by reading the exif data of the first jpg
    try:
        camera_name = get_camera_name(jpg_files[list(jpg_files.keys())[0]][0])

        if camera_name=='Canon EOS R5':
            camera_name='EOS_R5'

        print('Camera Name:',camera_name)
    except:
        print('Camera name could not be read.')
        camera_name = input('Camera Name: ')

    # get all unique dates to choose from
    unique_dates = list(sorted(set(jpg_files.keys())))

    # print and choose from unique dates
    print('Dates found:')
    for i,el in enumerate(unique_dates):

        try:
            n_photos = len(jpg_files[el])
        except KeyError:
            n_photos = 0

        try:
            n_videos = len(video_files[el])
        except KeyError:
            n_videos = 0

        print('[{:2}] {}  -> {:4} Photos, {:2} Videos'.format(i,el, n_photos, n_videos))

    str_date_indicies = input('Choose date(s): ') # multiple dates need spaces
    date_indicies = str_date_indicies.split()
    date_indicies = [int(el) for el in date_indicies]

    user_dates = []
    for el in date_indicies:
        user_dates.append(unique_dates[el])

    user_dates = sorted(user_dates)

    # input the title for that date
    # any spaces will be replaced with underscore
    user_title = input('Enter title: ')
    user_title = user_title.strip().replace(' ','_')

    # name of the upper directory

    if len(user_dates) == 1:
        dir_name = str(user_dates[0])+'_'+user_title
    else:
        dir_name = '{}_to_{}_{}'.format(user_dates[0], user_dates[-1], user_title)

    # make upper structure
    # date/cameraname
    camera_dir=os.path.join(dir_name, camera_name)
    make_dir_protected(dir_name)
    make_dir_protected(camera_dir)

    # make the lower directories and copy files
    # if user_date fails as a key in the dict, that means there are no files of that type for that date
    try:
        jpg_filenames = []
        for el in user_dates:
            jpg_filenames += jpg_files[el]

        jpg_dir = os.path.join(camera_dir, 'JPG')
        make_dir_protected(jpg_dir)
        copy_files(jpg_filenames, jpg_dir)

    except KeyError:
        print('No JPG files!')

    try:
        raw_filenames = []
        for el in user_dates:
            raw_filenames += raw_files[el]

        raw_dir = os.path.join(camera_dir, 'RAW')
        make_dir_protected(raw_dir)
        copy_files(raw_filenames, raw_dir)

    except KeyError:
        print('No RAW files!')

    try:
        video_filenames = []
        for el in user_dates:
            video_filenames += video_files[el]

        video_dir = os.path.join(camera_dir, 'Videos')
        make_dir_protected(video_dir)
        copy_files(video_filenames, video_dir)

    except KeyError:
        print('No video files!')

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('search_dir', type=str, help='Directory from which we are importing photos')
    parser.add_argument('-n', action='store_true', help='Ignores protection for import directory')
    args = parser.parse_args()

    pimport(args)

if __name__=='__main__':
    main()
