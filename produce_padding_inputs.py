#!/usr/local/bin/python2.7
#get a list of middle heptads and split them into pairs of 2
import os
from os import system,popen
import itertools
from sys import argv
import math
import numpy as np
import re
# import csv
# import matplotlib.pyplot as plt

lines = [line.rstrip('\n') for line in open(argv[1])]
combo_in=[]
for i in lines:
	i=re.split(' ',i) 
	combo_in.append(i[1])
#print combo_in
combo=itertools.combinations(combo_in, 2)
# for i in combo:
# 	print i
f=open("middle.list",'w')
for i in combo:
	#print i,"=="
	if i[0]!=i[1]:
		#print i,"======"
		f.write(i[0]+" "+i[1]+"\n")