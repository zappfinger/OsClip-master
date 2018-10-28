import os, time
from os import listdir
from os.path import isfile, join
from DBclass import *

entries=["c:/RBS/RBS SDS PCP UI", "/Users/richard/Downloads/testcases"]
#with os.scandir() as dir_entries:
#    for entry in dir_entries:
#        info = entry.stat()
#        print(info)

def getfilesindir(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for fil in onlyfiles:
        fp = join(mypath, fil)
        print(fil, "size: %s" % os.path.getsize(fp), "last modified: %s" % time.ctime(os.path.getmtime(fp)))
    return onlyfiles

def getall(mypath):
    allfiles = [f for f in listdir(mypath)]
    alls=''
    for all in allfiles:
        #fp = join(mypath, fil)
        #print(all)
        alls+=all + ';'
        #print(fil, "size: %s" % os.path.getsize(fp), "last modified: %s" % time.ctime(os.path.getmtime(fp)))
    return alls

if __name__ == '__main__':
    #getfilesindir(entries[1])
    print(getall('c:/'))