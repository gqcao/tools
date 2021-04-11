from numpy import *
import sys
sys.path.insert(0, '/home/gcao/Projects/retrieval/misc')
from fileproc import loadstr, writestr

def writeList():
    root_path = '/home/gcao/bash_cmd/mp3/'
    filenames = loadstr('mylist.txt')
    lst = []
    for f in filenames:
        lst.append('file ' + '\'' + root_path + f + '\'')
    writestr('mylist2.txt', lst)

if __name__ == '__main__':
    writeList()
