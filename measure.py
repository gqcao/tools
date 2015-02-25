#------------------------------------------------------------------------------------
# A piece of python code to demonstrate two common information retrieval measures:
# Discounted cumulative gain (DCG)
# and Averaged Normalized Modified Retrieval Rank (ANMRR)
#
# Created by Guanqun Cao (guanqun.cao@tut.fi)
# 25/02/2015
#------------------------------------------------------------------------------------

from numpy import *
import math
# import random

def generateData(type):
	data = []; sdata = []
	data.append(ones((20)))
	sdata.append(ones((20))) # all ones
	data.append(zeros((20)))
	sdata.append(zeros((20))) # all zeros
	if type == 'dcg':
		# generate random results.
		data.append(random.randint(0,4,size=20))
		sdata.append(sorted(data[2], reverse=True))
		data.append(random.randint(0,4,size=20))
		sdata.append(sorted(data[3], reverse=True))
		data.append(random.randint(0,4,size=20))
		sdata.append(sorted(data[4], reverse=True))
	elif type == 'anmrr':
		data.append(random.randint(0,2,size=20))
		sdata.append(sorted(data[2], reverse=True))
		data.append(random.randint(0,2,size=20))
		sdata.append(sorted(data[3], reverse=True))
		data.append(random.randint(0,2,size=20))
		sdata.append(sorted(data[4], reverse=True))
	return mat(data), mat(sdata)

def dcg(data, sdata):
	m,n = shape(data)
	dcg = mat(zeros(m))
	idcg = mat(zeros(m))
	for i in range(m):
		for j in range(n):
			dcg[0,i] = dcg[0,i] + (2 ** data[i, j] - 1) / math.log((j+2) , 2) # absolute dcg measure
			idcg[0,i] = idcg[0,i] + (2 ** sdata[i, j] - 1) / math.log((j+2) , 2) # ideal dcg measure
		dcg[0,i] = dcg[0,i] / idcg[0,i]
	return dcg

def anmrr(data):
	return

def evaluate(type, data, sdata):
	measure = []
	if type == 'dcg':
		measure = dcg(data, sdata)
	elif type == 'anmrr':
		measure = anmrr(data)
	return measure

if __name__=='__main__':
	type = 'dcg'
	data, sdata = generateData(type)
	print data
	# print sdata
	measure = evaluate(type, data, sdata)
	print type + ' accuracy=', measure
