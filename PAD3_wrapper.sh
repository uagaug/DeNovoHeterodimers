#1 is a list of sides that can accomodate more than 2 backbones. It is the result of `cat filtered.txt |awk '{print $1}' |uniq -c |gawk '$1>=2{print $2}' >more_than_2.txt`
#2 is the number of residues per repeat (7, 11, 18)
#for now I am doing it automatically, so $1 is the list after RMSD filter
dir=`pwd`
cat $1 |awk '{print $1}' |uniq -c |gawk '$1>=2{print $2}' >more_than_2.txt
echo "$1"
for i in `cat more_than_2.txt`;do 
	echo "working on $i"
	#actual padding goes here
	grep $i *filtered.txt >temp.list
	jj=${i//_sides.pdb/};full=${jj//sides/}; #get the full version of sides
	python /work/zibochen/scripts/helical_bundle/produce_padding_inputs.py temp.list #produce all possible combos for padding, in case there are more than 2 middels that go to one side.pdb
	for j in `cat middle.list `;do echo $j|awk '{print $0}';done |sort -u >uniq_middle #get ready for TMalign_rot
	for k in `cat uniq_middle`;do perl ~zibochen/bin/tmalign_rot.pl $k $i ${k//\/};done #align middle to sides
	#sed -i 's/TER//g' $full #remove TER, otherwise TMalign will stop at the first TER
	while IFS='' read -r line || [[ -n "$line" ]]; do
		in1=`echo $line|awk '{print $1}'`
		in2=`echo $line|awk '{print $2}'`
		#echo ${in1//\/}-${i//\/} ${in2//\/}-${i//\/} $full
		sh ~zibochen/scripts/helical_bundle/TMalign_index_pad3.sh ${in1//\/} ${in2//\/} $full $2
	done <middle.list
	#find `pwd` -name "*pdb_sides.pdb" -exec rm {} \;
	rm $dir/*middle?.pdb
done
rm temp.list middle.list uniq_middle