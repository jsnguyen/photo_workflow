import os
from datetime import datetime
import argparse

from pimport import make_dir_protected

##########################################################################
# Description:
# Makes the photo folder structure without copying anything

# Usage:
# python3 ./pwmakef.py <search_dir>
##########################################################################

# no automatic copying, doesn't copy anything
# takes user input to make the directory structure
def pfmake(args):

    usr_date = input("Enter date in YYYY-MM-DD format: ")

    try:
        usr_datetime_obj = datetime.strptime(usr_date,'%Y-%m-%d')
    except ValueError:
        raise Exception('Invalid date! Exiting...')

    print(usr_date)

    usr_title = input("Enter title of folder: ")
    user_dir = usr_date+'_'+usr_title

    make_dir_protected(user_dir)

    camera_name = input('Camera Name: ')
    camera_dir=os.path.join(user_dir,camera_name)
    make_dir_protected(camera_dir)

    dir_names = []

    if not args.nojpg:
        dir_names.append('JPG')
    if not args.noraw:
        dir_names.append('RAW')
    if not args.novideo:
        dir_names.append('Videos')

    user_dir=[os.path.join(camera_dir,fn) for fn in dir_names]

    for ud in user_dir:
        make_dir_protected(ud)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-j', '--nojpg', help='No JPG folder')
    parser.add_argument('-r', '--noraw', help='No RAW folder')
    parser.add_argument('-v', '--novideo', help='No Video folder')
    args = parser.parse_args()

    pfmake(args)

if __name__=='__main__':
    main()
