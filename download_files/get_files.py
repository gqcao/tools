#!/usr/bin/python

import subprocess
import mechanicalsoup
import urllib
from time import sleep
from pdb import set_trace
import re

if __name__ == '__main__':
    root_path = "/home/gcao/Lectures/mlops/"
    br = mechanicalsoup.StatefulBrowser()
    # Open your site
    br.open("https://ckaestne.github.io/seai/")
    suffix = [".pdf"]
    myfiles = []
    for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
        for t in suffix:
            if t in str(l): 
                myfiles.append(l)
    base_url = br.get_url()
    #base_url = "/".join(base_url.split("/")[:-1]) + "/"
    for l in myfiles:
        command = "cd "+ root_path +"; " +  "curl -O -J -L " + l.attrs['href'] # redirect links to real filenames
        subprocess.call(command, shell=True)
        print("Downloaded " + l.attrs['href'])
