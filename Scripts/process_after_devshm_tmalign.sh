ls -d *_*_* >dir_list
for i in `cat dir_list`;do cat $i/sides/*out >$i-TMalign_results.txt; awk '{ if ($5 >= 36 && $6 <= 0.3) print $1 " " $2 " " $3 " " $4 " " $5 " "$6}' $i-TMalign_results.txt > $i-filtered.txt;rm $i-TMalign_results.txt;done
#for i in `cat dir_list`;do cat $i/sides/*out | awk '{ if ($5 >= 36 && $6 <= 0.1) print $1 " " $2 " " $3 " " $4 " " $5 " "$6}' > $i-filtered.txt;done
