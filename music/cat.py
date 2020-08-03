from numpy import *
import sys
sys.path.insert(0, '/homeappl/home/gcao/fa/misc')
from fileproc import loadstr, writestr

def writeList():
    filenames = loadstr('mylist.txt')
    lst = []
    for f in filenames:
        lst.append('file ' + '\'' + '/wrk/gcao/misc/music/lyq/' + f + '\'')
    writestr('mylist2.txt', lst)

if __name__ == '__main__':
    writeList()
