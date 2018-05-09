# DeNovoHeterodimers
To generate heterodimer backboens with the heptad padding method:
1. For initial heptad sampling, run setup_parallel.sh which calls initial_HBNet_search.xml
2. To generate heptad chain ordering varints and prepare for TMalign, run
  		for j in `cat <list>`;do cd $j;mkdir middles sides;for i in *pdb;do python heptad_padding.py $i $i <layer (2, 3, or 5)>;done;cd ../;done &
3. Use perl ../bob.pl >p_do o generate run scripts for TMalign
4. sh process_after_devshm_tmalign.sh to filter for good TMalign-ed heptads onto backbones
5. sh PAD3_wrapper.sh *filtered.txt <number of residues per repeat (7, 11, 9 (because only sampling 9 residues for 5layer))> >log &   #this pads heptads into 3-network bundles

