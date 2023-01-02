import os
import pathlib

def avail_storage(path='/'):
    '''
    gets the available storage in bytes
    '''

    statvfs = os.statvfs(path)

    #statvfs.f_frsize * statvfs.f_blocks  # Size of filesystem in bytes
    #statvfs.f_frsize * statvfs.f_bfree   # Actual number of free bytes
    avail_bs = statvfs.f_frsize * statvfs.f_bavail  # Number of free bytes that ordinary users are allowed to use (excl. reserved space)

    return avail_bs

def best_denomination(bs):
    '''
    gets the best denomination of bytes kB, MB, or GB, will do GB by default
    does not truncate
    '''

    bs_kB = bs*1e-3
    bs_MB = bs*1e-6
    bs_GB = bs*1e-9

    if bs_MB < 1:
        return bs_kB, 'kB'

    if bs_GB < 1:
        return bs_MB, 'MB'

    return bs_GB, 'GB'

def get_file_size(filename):
    '''
    return the file size of a single file in bytes
    '''

    return pathlib.Path(filename).stat().st_size
