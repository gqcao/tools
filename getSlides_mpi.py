#!/usr/bin/env python
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Create parallel bots to download files from a website
# Now it can get files synchronously
# updated on 21/03/2015
# Send once from the master process and receive once from the slaves.
# TODO: has some problem with the scatter data type
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import subprocess
from time import sleep
from numpy import *
from mpi4py import MPI
import mechanize

comm = MPI.COMM_WORLD

def master():
	print "master"
	br = mechanize.Browser()
	folder_name = "ir" 
	command = "mkdir " + folder_name # create a new folder
	# Open your site
	br.open('http://www.stat.cmu.edu/~larry/=stat705/')

	suffix = ["homework", "Solutions"] #you will need to do some kind of pattern matching on your files
	myfiles = []
	for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
		for t in suffix:
			if t in str(l): 
				myfiles.append(l)
	ntasks = comm.Get_size();
        ntasks_ = ntasks - 1
	if ntasks_ >= len(myfiles):
		for l in myfiles:
			comm.send(l, rank + 1, tag = 11)
	elif ntasks_ < len(myfiles):
		rem = len(myfiles) % ntasks_
		for i in range(ntasks_):
			if rem > 0 and i < rem:
				links = myfiles[rem + i  * (len(myfiles) / ntasks_):rem + (i + 1) * (len(myfiles) / ntasks_) ]
				links.append(myfiles[i])
				comm.send(links, i + 1, tag=11)
			else:
				links = myfiles[rem + i  * (len(myfiles) / ntasks_):rem + (i + 1) * (len(myfiles) / ntasks_) ]
				comm.send(links, i + 1, tag=11)

def slave(folder_name):
	print "slave -gelen"
	links = comm.recv(source=0,tag = 11)
	# sleep(5) #throttle so you dont hammer the site
	# downloadlink(l)
	for l in links:
		command = "cd "+ folder_name +"; wget " + l.base_url + l.url 
		subprocess.call(command, shell=True)
		print "Downloaded" + l.url 

if __name__ == '__main__':
	# print myfiles
	# readNames()
	# subprocess.call("cd ~/bash_code; sh pltr_batch2.sh", shell=True)   
	folder_name = "/homeappl/home/gcao/AllOfStatistics/" 
        myrank = comm.Get_rank()
        if myrank == 0:
                master()
        else:
                slave(folder_name)
