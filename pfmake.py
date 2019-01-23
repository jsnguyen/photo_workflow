import os

usr_date = input("Enter date in MMDDYY format: ")
usr_title = input("Enter title of folder: ")
path = usr_date+'_'+usr_title

try:
    os.mkdir(path)
except:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)


subpath=path+'/D610'

try:
    os.mkdir(subpath)
except:
    print("Creation of the directory %s failed" % subpath)
else:
    print("Successfully created the directory %s " % subpath)

subsubpath=[subpath+'/RAW',subpath+'/JPG']

for p in subsubpath:
    try:
        os.mkdir(p)
    except:
        print("Creation of the directory %s failed" % p)
    else:
        print("Successfully created the directory %s " % p)
