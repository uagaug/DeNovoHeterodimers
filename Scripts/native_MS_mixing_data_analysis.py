# post native MS mixing experiment data analysis
# Zibo Chen, zibochen@uw.edu, Mar 2 2018
# Usage: python native_MS_mixing_data_analysis.py mass_tolerance time_cutoff [ms_list] [CID_mass_list] [theoretical_mass_list]
# Input format:
# ms_list: [time mass intensity]
# 1.7	9327.22	9.30E+05
# 1.7	9367.37	6.70E+05
# 1.7	9961.19	6.57E+05
# 1.7	18695.69	5.31E+05
# 1.7	9341.76	4.04E+05

# CID_mass_list: [time mass intensity]
# 1.62	8708.73	2.38E+05
# 1.62	9327.67	2.06E+05
# 1.62	9367.94	1.98E+05
# 1.62	9960.69	1.40E+05
# 1.62	9348.26	1.22E+05
# 1.62	8837.57	9.00E+04
# 1.62	8730.74	7.97E+04

# theoretical_mass_list: [design_name chain(+M) mass]
# 13 A 9328
# 13 B 9368
# 13_N15 A 9443
# 13_N15 B 9959
# 135 A 9320
# 135 B+M 8804

#import pandas as pd
#import numpy as np
from os.path import splitext 
#import matplotlib.pyplot as plt
#import seaborn as sns
from sys import argv
#import csv
import itertools

def find_initial_hits(observed_mass,mass_dict,mass_tolerance):
    list_of_hits=[]
    for key in mass_dict:
        if (abs(observed_mass-key)<mass_tolerance): 
            list_of_hits.append(list(itertools.chain(*mass_dict[key]))) #append flattened list
    return list_of_hits

def find_corresponding_monomers(time_cutoff,ms_list_line,pair,ms_list,cid_list,all_monomer_mass_dict,mass_tolerance): #third input is a pair of monomers
    found_hits=False
    time=float(ms_list_line[0])
    time_in_a_bottle=[]
    monomer_one_mass=float(all_monomer_mass_dict[pair[0]])
    monomer_one_hit=False
    monomer_two_mass=float(all_monomer_mass_dict[pair[1]])
    monomer_two_hit=False
    for i in ms_list:
        if abs(time-float(i[0]))<time_cutoff:
            time_in_a_bottle.append(i)
    for i in cid_list:
        if abs(time-float(i[0]))<time_cutoff:
            time_in_a_bottle.append(i)
    if len(time_in_a_bottle)>0:
        for i in time_in_a_bottle:
            if abs(float(i[1])-monomer_one_mass)<mass_tolerance:
                monomer_one_hit=True
            if abs(float(i[1])-monomer_two_mass)<mass_tolerance:
                monomer_two_hit=True
    if (monomer_one_hit and monomer_two_hit):
        found_hits=True
    return found_hits
    
mass_tolerance=float(argv[1]) #default is 2 Da
time_cutoff=float(argv[2]) #default is 1 min
ms_list_file=open(argv[3])
cid_list_file=open(argv[4])
theo_list_file=open(argv[5])

# mass_tolerance=2
# time_cutoff=1
# ms_list_file=open("ms.txt")
# cid_list_file=open("cid.txt")
# theo_list_file=open("masslist.txt")

ms_list=[i.rstrip().split() for i in ms_list_file.readlines()]
cid_list=[i.rstrip().split() for i in cid_list_file.readlines()]
theo_list=[i.rstrip().split() for i in theo_list_file.readlines()]

all_monomer_mass_dict={} #13_A:9639
all_dimer_mass_dict={} #19081:[13_A,15_B]
ms_max_intensity=max([float(sublist[2]) for sublist in ms_list])

#generate monomer and all possible dimer masses
for i in range(len(theo_list)):
    #update monomer mass list
    all_monomer_mass_dict[theo_list[i][0]+"_"+theo_list[i][1]]=theo_list[i][2]
    #update dimer mass list
    for j in range(i,len(theo_list)):
        temp_mass=float(theo_list[i][2])+float(theo_list[j][2])
        if temp_mass in all_dimer_mass_dict:
            all_dimer_mass_dict[temp_mass].append([theo_list[i][0]+"_"+theo_list[i][1],theo_list[j][0]+"_"+theo_list[j][1]])
        else:
            all_dimer_mass_dict[temp_mass]=[[theo_list[i][0]+"_"+theo_list[i][1],theo_list[j][0]+"_"+theo_list[j][1]]]

#find all hits within intensity and mass tolerance
for i in ms_list:
    if (float(i[2])/ms_max_intensity)>0.01: #only consider intensities > 1% of maximum intensity
        temp_hits=find_initial_hits(float(i[1]),all_dimer_mass_dict,mass_tolerance)
        if len(temp_hits)>0: #only proceed to CID search if there is a hit
            for j in temp_hits:
                if find_corresponding_monomers(time_cutoff,i,j,ms_list,cid_list,all_monomer_mass_dict,mass_tolerance): #perform CID search
                    print (j,i)                    