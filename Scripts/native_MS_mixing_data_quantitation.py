# post native MS mixing experiment data analysis, now quantitating off-diagonal exchanges
# Zibo Chen, zibochen@uw.edu, Mar 19 2018
# Run it after native_MS_mixing_data_analysis.py
# Need to manually process:
# Theoretical list file to only contain proteins of interest. It should also be sorted.
# non-denaturing files to only contain cognate (on-diagonal) pairs
##############################
#######IMPORTANT##############
# Assumption is that there is no exchange in the non-denaturing run. Please double check input files to make sure!
##############################
#######IMPORTANT##############

# Best to run with Python2
# Usage: python native_MS_mixing_data_quantitation.py [theoretical_mass_list] [Non-denaturing_data1] [Non-denaturing_data2] [Denaturing_data1] [Denaturing_data2]
# Input format:
# theoretical_mass_list: [design_name chain(+M) mass]
# 13 A 9328
# 13 B 9368
# 13_N15 A 9443
# 13_N15 B 9959
# 135 A 9320
# 135 B+M 8804

# Non-denaturing data: ([Chain A, Chain B], [time, mass, intensity])
# (['39_A', '39_B'], ['1.76', '25952.24', '6.16E+06'])
# (['37_21_A', '37_21_B'], ['1.76', '17570.19', '5.39E+06'])
# (['37_31_A', '37_31_B'], ['1.76', '17791.82', '3.85E+06'])
# (['13_A', '13_B'], ['1.76', '18695.17', '1.47E+06'])
# (['13_N3C1_A', '13_N3C1_B'], ['2.7', '18343.86', '6.77E+07'])
# (['13_31_A', '13_31_B'], ['7.99', '18775.23', '1.07E+06'])
# (['13_31_A', '13_31_B'], ['10.96', '18774.42', '1.06E+06'])
# (['13_31_A', '13_31_B+M'], ['11.88', '18907.28', '1.86E+07'])

# Denaturing data: same as above

import pandas as pd
import numpy as np
#from os.path import splitext 
import matplotlib.pyplot as plt
import seaborn as sns
from sys import argv
#import itertools
import re

def clean_up(in_str):
    for ch in ['(',')','[',']','\'',',']:
        if ch in in_str:
            in_str=in_str.replace(ch," ")
    return in_str

def get_list_from_file(in_file):
    list_temp=[clean_up(i.rstrip()) for i in in_file.readlines()]
    out_list=[]
    for i in list_temp:
        out_list.append(i.split())
    return out_list

def get_nondenature_dict(in_list):
    nondenature_intensity_dict={}
    for i in in_list:
        # does not consider off-target binding as well as homodimers
        if ((((i[0].split("+"))[0])[:-2] == ((i[1].split("+"))[0])[:-2]) and (i[0] != i[1])):
            design_name=((i[0].split("+"))[0])[:-2]
            if (design_name in nondenature_intensity_dict):
                nondenature_intensity_dict[design_name][2]+=float(i[4])
            else:
                nondenature_intensity_dict[design_name]=[design_name+"_A",design_name+"_B",float(i[4])]
    return nondenature_intensity_dict

def get_denature_dict(in_list):
    denature_intensity_dict={}
    for i in in_list:
        des1_name=((i[0].split("+"))[0])
        des2_name=((i[1].split("+"))[0])
        name_list=[des1_name,des2_name]
        name_list.sort()
        combined_name=name_list[0]+"---"+name_list[1]
        if combined_name in denature_intensity_dict:
            denature_intensity_dict[combined_name][3]+=float(i[4])
        else:
            denature_intensity_dict[combined_name]=[combined_name,name_list[0][:-2],name_list[1][:-2],float(i[4])]
    return denature_intensity_dict

def combinde_nondenature_dict(dict1,dict2):
    for i in dict2.keys():
        if i in dict1:
            dict1[i][2]=max(dict1[i][2],dict2[i][2])
        else:
            dict1[i]=dict2[i]
    return dict1

def combinde_denature_dict(dict1,dict2):
    for i in dict2:
        if i in dict1:
            dict1[i][3]=max(dict1[i][3],dict2[i][3])
        else:
            dict1[i]=dict2[i]
    return dict1
    
# theo_list_file=open("theo_mass2.txt")
# nondenature_list_file=open("hit_N_wcx_8k.txt")
# nondenature_list_file2=open("hit_N_wax_8k.txt")
# denature_list_file=open("hit_DN_wcx_8k.txt")
# denature_list_file2=open("hit_DN_wax_8k.txt")

theo_list_file=open(argv[1])
nondenature_list_file=open(argv[2])
nondenature_list_file2=open(argv[3])
denature_list_file=open(argv[4])
denature_list_file2=open(argv[5])

#The purpose of theo_list_file as input is to get design names. One can just have proteins of interest in this file and designs not
#in this file will not be considered in the heatmap calculation.
theo_list=[i.rstrip().split() for i in theo_list_file.readlines()]
des_name_list=[]
for i in theo_list:
    if i[0] not in des_name_list:
        des_name_list.append(i[0])

#clean up inputs 2 and 3 and 4 and 5
nondenature_list=get_list_from_file(nondenature_list_file)
denature_list=get_list_from_file(denature_list_file)
nondenature_list2=get_list_from_file(nondenature_list_file2)
denature_list2=get_list_from_file(denature_list_file2)

#For the non-denatured, I am treating A+M and A, B+M and B as the same and summing their intensities as the final intensity of the heterodimer
nondenature_intensity_dict=get_nondenature_dict(nondenature_list)
nondenature_intensity_dict2=get_nondenature_dict(nondenature_list2)

#Now combine nondenature_intensity_dict and nondenature_intensity_dict2. For the species that appears in both lists, take the bigger value.
combined_nondenature_intensity_dict=combinde_nondenature_dict(nondenature_intensity_dict,nondenature_intensity_dict2)

#Doing the same for the denatured
denature_intensity_dict=get_denature_dict(denature_list)
denature_intensity_dict2=get_denature_dict(denature_list2)
combined_denature_intensity_dict=combinde_denature_dict(denature_intensity_dict,denature_intensity_dict2)

#Construct the 2D matrix
col_name=[]
for i in des_name_list:
    col_name.append(i+"_A")
    col_name.append(i+"_B")
df = pd.DataFrame(np.zeros((len(col_name), len(col_name))), index=col_name, columns=col_name)

#Now figure out the relative intensity
# find DN(i)(A) in the N(j)(A) and use DN(i)(rA_intensity)=DN(i)(intensity)/N(i)(intensity);
# find DN(i)(B) in the N(j)(B) and use DN(i)(rB_intensity)=DN(i)(intensity)/N(i)(intensity);
# DN(i)(r_intensity)=(DN(i)(rA_intensity)+DN(i)(rB_intensity))/2
for i in combined_denature_intensity_dict:
    #Only consider designs included in the theoretical mass list
    if ((combined_denature_intensity_dict[i][1] in des_name_list) and (combined_denature_intensity_dict[i][2] in des_name_list)):
        #make sure the corresponding cognate heterodimer is detected in the non-denaturing condition
        if ((combined_denature_intensity_dict[i][1] in combined_nondenature_intensity_dict) and (combined_denature_intensity_dict[i][2] in combined_nondenature_intensity_dict)):
            first_binder_name=combined_denature_intensity_dict[i][1]
            native_intensity_1=combined_nondenature_intensity_dict[first_binder_name][2]
            relative_intensity_1=combined_denature_intensity_dict[i][3]/native_intensity_1
            second_binder_name=combined_denature_intensity_dict[i][2]
            native_intensity_2=combined_nondenature_intensity_dict[second_binder_name][2]
            relative_intensity_2=combined_denature_intensity_dict[i][3]/native_intensity_2
            ave_intensity=0.5*(relative_intensity_1+relative_intensity_2)
            binders=combined_denature_intensity_dict[i][0].split("---")
            df.loc[binders[0],binders[1]]=ave_intensity
            df.loc[binders[1],binders[0]]=ave_intensity #make the matrix symmetric
        else:
            if (combined_denature_intensity_dict[i][1] not in combined_nondenature_intensity_dict):
                print (combined_denature_intensity_dict[i][1]+" not detected in the non-denaturing mix!")
            else:
                print (combined_denature_intensity_dict[i][2]+" not detected in the non-denaturing mix!")

plt.clf()
writer = pd.ExcelWriter('Relative_intensity.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
sns.heatmap(df,cmap="YlGnBu",square=1,cbar_kws={'label': 'Relative Inrensity'})
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.savefig("2D_heatmap.svg", format='svg',transpatent=True)
plt.savefig("2D_heatmap.png",transpatent=True)