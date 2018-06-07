#wrapper script for finding alignment indecies
#input 1 is the middle heptad already aligned to sides, input 3 is the full target pose for the middle heptad to fall onto
#input 2 is the 3rd middle heptad already aligned to sides
#input 4 is the number of residues per repeat (7, 11, 18)
index_string=`perl ~zibochen/scripts/helical_bundle/get_seq_aln.pl $1 $3|head -1`
indecies=`python /work/zibochen/scripts/helical_bundle/TMalign_index.py $index_string $4`
index_string2=`perl ~zibochen/scripts/helical_bundle/get_seq_aln.pl $2 $3|head -1`
indecies2=`python /work/zibochen/scripts/helical_bundle/TMalign_index.py $index_string2 $4`
#check for residue clashes
#python /work/zibochen/scripts/helical_bundle/pad_helices_check_clash.py $indecies $indecies2
check=`python /work/zibochen/scripts/helical_bundle/pad_helices_check_clash.py $indecies $indecies2 $4`
#check=1 if there is no residue clash
n0=1
let n1=$n0+$4
let n2=$n1+$4
let n3=$n2+$4
if (("$check" > 0)); then \
	#echo "/work/zibochen/Rosetta_devel/main/source/bin/pad_helices.default.linuxgccrelease -s $1 $3 $2 -span $4 -src_pose_1_start $n0,$n1,$n2,$n3 -target_pose_start $indecies -prefix $1-$2- -pad_3_heptads true -target_pose_start_2 $indecies2;"
	/work/zibochen/Rosetta_devel/main/source/bin/pad_helices.default.linuxgccrelease -mute all -s $1 $3 $2 -span $4 -src_pose_1_start $n0,$n1,$n2,$n3 -target_pose_start $indecies -prefix $1-$2- -pad_3_heptads true -target_pose_start_2 $indecies2;\
else \
	echo $1" and "$2 "clashing on "$3;\
fi;
#/work/zibochen/Rosetta_devel/main/source/bin/pad_helices.default.linuxgccrelease -s $1 $3 $2 -src_pose_start 1,8,15,22 -target_pose_start $indecies -prefix $4 -pad_3_heptads true -target_pose_start_2 $indecies2