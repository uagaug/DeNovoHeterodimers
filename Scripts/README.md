# DeNovoHeterodimers
## To generate heterodimer backboens with the heptad padding method
1. For initial heptad sampling, run setup_parallel.sh which calls initial_HBNet_search.xml
2. To generate heptad chain ordering varints and prepare for TMalign, run
  		"for j in `cat <list>`;do cd $j;mkdir middles sides;for i in *pdb;do python heptad_padding.py $i $i <layer (2, 3, or 5)>;done;cd ../;done &"
3. Use perl ../bob.pl >p_do to generate run scripts for TMalign
4. sh process_after_devshm_tmalign.sh to filter for good TMalign-ed heptads onto backbones
5. sh PAD3_wrapper.sh *filtered.txt <number of residues per repeat (7, 11, 9 (because only sampling 9 residues for 5layer))> >log &   #this pads heptads into 3-network bundles

## Loop closure
rosetta_scripts.hdf5.linuxgccrelease @loop_closure.flags

## Final design
rosetta_scripts.hdf5.linuxgccrelease @heterodimer_final_design_only_design.flags -in:file:s $in_pdb

## Native MS data analysis
1. To identify exchanged monomers: python native_MS_mixing_data_analysis.py mass_tolerance time_cutoff ms_list CID_mass_list theoretical_mass_list
2. To quantify exchanged monomers: python native_MS_mixing_data_quantitation.py theoretical_mass_list Non-denaturing_data1 Non-denaturing_data2 Denaturing_data1 Denaturing_data2

## Script for NUS processing (4D-HNCH-TOCSY)
NMR_process.sh
