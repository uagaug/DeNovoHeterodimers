#!/usr/local/bin/python2.7
#given two helical bundles with 5 heptads each, could the middle heptad from Bundle 1 align to the outer 4 heptads of Bundle 2?
from os import system,popen
import itertools
from sys import argv
import math
import numpy as np
import re
# import csv
# import matplotlib.pyplot as plt

def extract_sub_pdb(infile,outfile,start,end):
	hits=[]
	with open(infile) as template:
		for line in template:
			for i in range(start,end+1):
				find_this=str(i)
				if line.startswith("ATOM"):
					if find_this==line[22:26].strip():
						hits.append(line)
	f = open(outfile, 'a')
	for i in hits:
		f.write(i)
	f.close

def combo(prefix,infile):
	#save each chain to lists
	chainA=[]
	chainB=[]
	chainC=[]
	chainD=[]
	with open(infile) as template:
		for line in template:
			if line.startswith("ATOM"):
				if "A"==line[21]:
					chainA.append(line)
				elif "B"==line[21]:
					chainB.append(line)
				elif "C"==line[21]:
					chainC.append(line)
				elif "D"==line[21]:
					chainD.append(line)
	f = open(prefix+"middle2.pdb", 'w')
	for i in chainA:
		f.write(i)
	for i in chainB:
		f.write(i)
	for i in chainD:
		f.write(i)
	for i in chainC:
		f.write(i)
	f.close
	f = open(prefix+"middle3.pdb", 'w')
	for i in chainA:
		f.write(i)
	for i in chainD:
		f.write(i)
	for i in chainB:
		f.write(i)
	for i in chainC:
		f.write(i)
	f.close
	f = open(prefix+"middle4.pdb", 'w')
	for i in chainA:
		f.write(i)
	for i in chainD:
		f.write(i)
	for i in chainC:
		f.write(i)
	for i in chainB:
		f.write(i)
	f.close
	f = open(prefix+"middle5.pdb", 'w')
	for i in chainA:
		f.write(i)
	for i in chainC:
		f.write(i)
	for i in chainD:
		f.write(i)
	for i in chainB:
		f.write(i)
	f.close
	f = open(prefix+"middle6.pdb", 'w')
	for i in chainA:
		f.write(i)
	for i in chainC:
		f.write(i)
	for i in chainB:
		f.write(i)
	for i in chainD:
		f.write(i)
	f.close

if __name__=="__main__":
	from_pdb=argv[1]+"_"
	to_pdb=argv[2]+"_"
	layer=argv[3]
	#getting the middle heptad
	if layer=='2':
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",15,21)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",50,56)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",85,91)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",120,126)
		#getting the outer heptads
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",1,14)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",22,35)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",36,49)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",57,70)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",71,84)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",92,105)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",106,119)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",127,140)
	elif layer=='3':
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",12,22)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",45,55)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",78,88)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",111,121)
		#getting the outer heptads
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",1,11)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",23,33)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",34,44)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",56,66)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",67,77)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",89,99)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",100,110)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",122,132)
	elif layer=='5.1':
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",10,18)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",46,54)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",91,99)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",127,135)
		#getting the outer heptads
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",1,9)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",19,36)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",37,45)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",55,72)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",73,90)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",100,108)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",109,126)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",136,144)
	elif layer=='5.2':
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",19,27)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",55,63)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",82,90)
		extract_sub_pdb(argv[1],from_pdb+"middle1.pdb",118,126)
		#getting the outer heptads
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",1,18)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",28,36)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",37,54)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",64,72)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",73,81)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",91,108)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",109,117)
		extract_sub_pdb(argv[2],to_pdb+"sides.pdb",127,144)
	#permutate the combinations of chains in middle.pdb for TMalign
	combo(from_pdb,from_pdb+"middle1.pdb");
	#TMalign middle to sides
	#cmd="/work/dadriano/DEVEL/netMotif_v0.2b/mican_netMotif_2014.12.29/mican_netMotif middle.pdb sides.pdb"
	#cmd="~krypton/bin/TMalign middle1.pdb sides.pdb"
	#system(cmd)
	#cmd="rm middle*.pdb sides.pdb"
	#system(cmd)
	cmd="mv *middle*.pdb middles"
	system(cmd)
	cmd="mv *sides.pdb sides"
	system(cmd)