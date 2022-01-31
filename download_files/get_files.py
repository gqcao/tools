#!/usr/bin/python

import subprocess
import mechanicalsoup
import urllib
from time import sleep
from pdb import set_trace
import re

if __name__ == '__main__':
    root_path = "/home/gcao/Lectures/embedded_system/"
    br = mechanicalsoup.StatefulBrowser()
    # Open your site
    br.open("https://users.ece.cmu.edu/~koopman/ece642_OLD/index.html")
    suffix = [".pdf"]
    myfiles = []
    for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
        for t in suffix:
            if t in str(l): 
                myfiles.append(l)
    base_url = br.get_url()
    base_url = "/".join(base_url.split("/")[:-1]) + "/"
    for l in myfiles:
        command = "cd "+ root_path +"; " +  "curl -O -J -L " + base_url + l.attrs['href'] # redirect links to real filenames
        subprocess.call(command, shell=True)
        print("Downloaded " + l.attrs['href'])
