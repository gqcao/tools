#!/usr/bin/python

import subprocess
import mechanicalsoup 
from time import sleep
from pdb import set_trace
import re

def downloadlink(l):
    f=open(l.text,"w") #perhaps you should open in a better way & ensure that file doesn't already exist.
    br.click_link(l)
    f.write(br.response().read())
    print(l.text," has been downloaded")

def readNames():      # general function to parse tab-delimited floats
    fileName = "names"
    chapters = []
    cnt = 0
    with open(fileName) as fr:
        for line in fr:
            curLine = line.strip().split()
            chapters.append(curLine[0])
    # print chapters
    chaptersFull = []
    header = "http://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/"
    for i in range(len(chapters)):
        if i < 10:
            chaptersFull.append(header + "0" + str(i) + chapters[i] +  "-2x2.pdf")
        elif i >= 10:
            chaptersFull.append(header + str(i) + chapters[i] + "-2x2.pdf")
    print(chaptersFull)
    return chapters

if __name__ == '__main__':
    root_path = "/home/gcao/tmp/"
    br = mechanicalsoup.StatefulBrowser()
    # Open your site
    br.open("http://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/")
    suffix = [".xlsx"] #you will need to do some kind of pattern matching on your files
    myfiles = []
    print(br.links())
    for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
        for t in suffix:
            if t in str(l): 
                myfiles.append(l)
    base_url = br.get_url() 
    #base_url = re.sub('lecture_slides.html', '', br.get_url())
    for l in myfiles:
        # sleep(5) #throttle so you dont hammer the site
        # downloadlink(l)
        #command = "cd "+ root_path +"; " +  "wget " + l.attrs['href']
        command = "cd "+ root_path +"; " +  "wget " + base_url + l.attrs['href']
        subprocess.call(command, shell=True)
        print("Downloaded " + l.attrs['href'])
        print(l.text)
    # readNames()
    # subprocess.call("cd ~/bash_code; sh pltr_batch2.sh", shell=True)    
