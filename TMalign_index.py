#!/usr/local/bin/python2.7
#get the alignment regions for TMalign of heptads
import os
from os import system,popen
import itertools
from sys import argv
import math
import numpy as np
import re
# import csv
# import matplotlib.pyplot as plt

#find indicies of all the letters, and deduce indicies of the starting points

string=argv[1]
repeat=int(argv[2])
hits=[]
vec=[]
final=[]
for i in range(len(string)-1):
	if ((string[i] != "-") and i==0): #take care of this case: SSSSSSS-----------
		hits.append(1)
	if ((string[i] == "-") and (string[i+1] != "-")):
		#print i
		hits.append(i+2)
	if ((string[i] != "-") and ((string[i+1] == "-")) or i==len(string)-2): #after or: take care of this case: ------SSSSSSS
		#print i
		hits.append(i+2)
#print len(hits)
for i in range((len(hits))/2):
	#print range(hits[2*i],hits[2*i+1])
	vec.extend(range(hits[2*i],hits[2*i+1]))
#print len(vec)
final.append(vec[0])
final.append(vec[repeat])
final.append(vec[repeat*2])
final.append(vec[repeat*3])

out=""
for i in final:
	out+=str(i)
	out+=","
ind=out[0:-1]
print ind