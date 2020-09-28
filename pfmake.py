#!/usr/local/bin/python3

import os
import pathlib
from datetime import datetime

usr_date = input("Enter date in YYYY-MM-DD format: ")

try:
    usr_datetime_obj = datetime.strptime(usr_date,'%Y-%m-%d')
except ValueError:
    raise Exception('Invalid date! Exiting...')

print(usr_date)

usr_title = input("Enter title of folder: ")
path = usr_date+'_'+usr_title

try:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
except:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)


subpath=os.path.join(path,'D610')

try:
    pathlib.Path(subpath).mkdir(parents=True, exist_ok=True)
except:
    print("Creation of the directory %s failed" % subpath)
else:
    print("Successfully created the directory %s " % subpath)

subsubfoldernames = ['RAW', 'JPG', 'Videos']
subsubpath=[os.path.join(subpath,fn) for fn in subsubfoldernames]

for p in subsubpath:
    try:
        pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    except:
        print("Creation of the directory %s failed" % p)
    else:
        print("Successfully created the directory %s " % p)
