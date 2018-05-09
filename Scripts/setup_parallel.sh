for delta_omega_1 in `seq $1 1 $1`;do
	for delta_omega_2 in `seq 0 10 90`;do
		for delta_omega_3 in `seq 0 10 90`;do
			for delta_omega_4 in `seq 0 10 90`;do
				for z1_offset_1 in `seq -1.51 1.51 1.51`;do
					for z1_offset_2 in `seq -1.51 1.51 1.51`;do
						for z1_offset_3 in `seq -1.51 1.51 1.51`;do
							for r_in_1 in `seq 5 1 6`;do
								for r_in_2 in `seq 6 1 8`;do
									for r_out_1 in `seq 7 1 9`;do
										for r_out_2 in `seq 8 1 9`;do
											echo "/suppscr/baker/sboyken/current_rosetta/Rosetta/main/source/bin/rosetta_scripts.default.linuxiccrelease @flags -parser:script_vars delta_omega_1=$delta_omega_1 delta_omega_2=$delta_omega_2 delta_omega_3=$delta_omega_3 delta_omega_4=$delta_omega_4 r_in_1=$r_in_1 r_in_2=$r_in_2 r_out_1=$r_out_1 r_out_2=$r_out_2 z1_offset_1=$z1_offset_1 z1_offset_2=$z1_offset_2 z1_offset_3=$z1_offset_3 -out:prefix "$delta_omega_1"_"$delta_omega_2"_"$delta_omega_3"_"$delta_omega_4"_"$z1_offset_1"_"$z1_offset_2"_"$z1_offset_3"_"$r_in_1"_"$r_in_2"_"$r_out_1"_"$r_out_2"_>/dev/null"
										done
									done
								done
							done
						done
					done
				done
			done
		done
	done
done >to_do_$1 &