#!/usr/bin/python

import subprocess
import mechanicalsoup 
from time import sleep
from pdb import set_trace
import re

if __name__ == '__main__':
    root_path = "/home/gcao/lectures/bayes_filter/"
    br = mechanicalsoup.StatefulBrowser()
    # Open your site
    br.open("https://mycourses.aalto.fi/course/view.php?id=24745&section=2")
    prefix = ["https://mycourses.aalto.fi/mod/resource/view.php?id="]
    myfiles = []
    for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
        for t in prefix:
            if t in str(l): 
                myfiles.append(l)
    base_url = br.get_url() 
    for l in myfiles:
        command = "cd "+ root_path +"; " +  "curl -O -J -L " + l.attrs['href'] # redirect links to real filenames
        subprocess.call(command, shell=True)
        print("Downloaded " + l.attrs['href'])
