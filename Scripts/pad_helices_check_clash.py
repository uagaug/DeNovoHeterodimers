#!/usr/local/bin/python2.7
#check for residue clashes in 3 heptad padding
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

pad1=argv[1]
pad2=argv[2]
repeat=int(argv[3])
ind1=[]
ind2=[]
for i in re.split(',',pad1):
	for j in range(repeat):
		ind1.append(int(i)+j)
for i in re.split(',',pad2):
	for j in range(repeat):
		ind2.append(int(i)+j)
ind1.extend(ind2)
#check for duplicates
if len(list(set(ind1)))<len(ind1):
	print 0 #clash
else:
	print 1 #no_clash