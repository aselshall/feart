#[1] Date period list

#(1.1) List for each model
#list year (One year period list)
LY=(CMCC-CM2-HR4_hist-1950_r1i1p1f1
	CMCC-CM2-VHR4_hist-1950_r1i1p1f1
	EC-Earth3P_hist-1950_r1i1p2f1
	EC-Earth3P_hist-1950_r2i1p2f1
	EC-Earth3P_hist-1950_r3i1p2f1
	EC-Earth3P-HR_hist-1950_r1i1p2f1
	EC-Earth3P-HR_hist-1950_r2i1p2f1
	EC-Earth3P-HR_hist-1950_r3i1p2f1
	ECMWF-IFS-HR_hist-1950_r1i1p1f1
	ECMWF-IFS-HR_hist-1950_r2i1p1f1
	ECMWF-IFS-HR_hist-1950_r3i1p1f1
	ECMWF-IFS-HR_hist-1950_r4i1p1f1
	ECMWF-IFS-HR_hist-1950_r5i1p1f1
	ECMWF-IFS-HR_hist-1950_r6i1p1f1
	ECMWF-IFS-MR_hist-1950_r1i1p1f1
	ECMWF-IFS-MR_hist-1950_r2i1p1f1
	ECMWF-IFS-MR_hist-1950_r3i1p1f1
	HadGEM3-GC31-HM_hist-1950_r1i1p1f1
	HadGEM3-GC31-HM_hist-1950_r1i3p1f1
	HadGEM3-GC31-HM_hist-1950_r1i2p1f1
	HadGEM3-GC31-MM_hist-1950_r1i1p1f1
	HadGEM3-GC31-MM_hist-1950_r1i2p1f1
	HadGEM3-GC31-MM_hist-1950_r1i3p1f1
	MPI-ESM1-2-HR_hist-1950_r1i1p1f1
	MPI-ESM1-2-XR_hist-1950_r1i1p1f1)
	
#List year _ list month (Three month list)
LY_LM=(HadGEM3-GC31-HH_hist-1950_r1i1p1f1)

#List period (5 year period)
LP05=(E3SM-1-0_historical_r1i1p1f1
		E3SM-1-0_historical_r2i1p1f1
		E3SM-1-0_historical_r3i1p1f1
		E3SM-1-0_historical_r4i1p1f1
		E3SM-1-0_historical_r5i1p1f1)

#List period (10 year period)
LP10=(CNRM-CM6-1-HR_hist-1950_r1i1p1f2
      CNRM-CM6-1-HR_hist-1950_r2i1p1f2
      CNRM-CM6-1-HR_hist-1950_r3i1p1f2)

#List period with one-based indix (count from 1 with 10 year period)
LP10o=(AWI-CM-1-1-MR_historical_r1i1p1f1
    	AWI-CM-1-1-MR_historical_r2i1p1f1
    	AWI-CM-1-1-MR_historical_r3i1p1f1
    	AWI-CM-1-1-MR_historical_r4i1p1f1
  		AWI-CM-1-1-MR_historical_r5i1p1f1)

#List period with one-based index missing last period (count from 1 with 10 year period)
LP10om=(AWI-CM-1-1-HR_hist-1950_r1i1p1f2)

#List period (20 year period)
LP20=(GFDL-CM4_historical_r1i1p1f1
		GFDL-ESM4_historical_r2i1p1f1
		GFDL-ESM4_historical_r3i1p1f1
		HadGEM3-GC31-MM_historical_r1i1p1f3
		HadGEM3-GC31-MM_historical_r2i1p1f3
		HadGEM3-GC31-MM_historical_r3i1p1f3
		HadGEM3-GC31-MM_historical_r4i1p1f3)

#List period (one file from 1950-2015)
LP1950=(CESM1-CAM5-SE-HR_hist-1950_r1i1p1f1)

#List period (one file from 1850-2015)
LP1850=(CNRM-CM6-1-HR_historical_r1i1p1f2)

#List for AVISO
LPA=(AVISO-1-0_BE_r0) #gn_199210-201012.nc

#(1.2) simuluation name
model_exp_sim=${model}_${exp}_${sim}


#(1.3) List creation
if [[ " ${LY[@]} " =~ " ${model_exp_sim} " ]]; then
	
	#List year (One year period list)	
	for yyyy in $(seq 1990 2014); do 
		list+=("${yyyy}01-${yyyy}12")
	done

elif [[ " ${LY_LM[@]} " =~ " ${model_exp_sim} " ]]; then
	
	#List year _ list month (Three month list)
	for yyyy in $(seq 1990 2014); do
		list+=("${yyyy}01-${yyyy}03")
		list+=("${yyyy}04-${yyyy}06")
		list+=("${yyyy}07-${yyyy}09")
		list+=("${yyyy}10-${yyyy}12")
	done

elif [[ " ${LP05[@]} " =~ " ${model_exp_sim} " ]]; then

	#List period (5 year period)
	list=(199001-199412 199501-199912 200001-200412 200501-200912 201001-201412)  

elif [[ " ${LP10[@]} " =~ " ${model_exp_sim} " ]]; then

	#List period (10 year period)
	list=(199001-199912 200001-200912 201001-201412)

elif [[ " ${LP10o[@]} " =~ " ${model_exp_sim} " ]]; then

	#List period with one-based index (10 year period)
	list=(198101-199012 199101-200012 200101-201012 201101-201412)

elif [[ " ${LP10om[@]} " =~ " ${model_exp_sim} " ]]; then

	#List period with one-based index missing last period (10 year period)
	list=(198101-199012 199101-200012 200101-201012)

elif [[ " ${LP20[@]} " =~ " ${model_exp_sim} " ]]; then	

	#list period (20 year period)
	list=(199001-200912 201001-201412)

elif [[ " ${LP1950[@]} " =~ " ${model_exp_sim} " ]]; then
	
	#List period (one file from 1950-2015)
	list=(195001-201412)

elif [[ " ${LP1850[@]} " =~ " ${model_exp_sim} " ]]; then

	#List period (one file from 1850-2015)
	list=(185001-201412)

elif [[ " ${LPA[@]} " =~ " ${model_exp_sim} " ]]; then
	
	#List period (one file from 199210-201012)
	list=(199210-201012)
	echo="Period 199210-201012"
fi

#(1.4) Annotation 
echo "${model_exp_sim} has ${#list[@]} files"



#[2] Process files (hyper-slab to GoM region and concatenate for total period

#Annotation
echo "Hyper-slab files"

#Loop to hyper-slab files
np=0
for period in ${list[@]}; do
	
	#Period counter for print to screen
	let "np+=1"
	
	#Path to input files
	if [[ ${model} == "E3SM-1-0" ]] ; then
		file=zos_Omon_"${model}"_"${exp}"_"${sim}"_gr_"${period}".nc
	else
		file=zos_Omon_"${model}"_"${exp}"_"${sim}"_gn_"${period}".nc
	fi
	in=Gmap/zos/$model/$exp/$file
	
	#Path to output files
	pathout="FLmap/zos/${folder}/raw/${model}/${exp}"
	mkdir -p ${pathout}
	out=${pathout}/${file}
	
	
	#Hyper-slab file
	#lon(i) index for longitude (260W to 285E)
	#lat(j) index for latitude (17S to 35N)
	#ncks -O -F -d i,750,850 -F -d j,597,681 $in $out
	#IDX=(750 850 597 681)
	#ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    if [[ ${model} == "AWI-CM-1-1-HR" ]] ; then
          echo "Re-gridding required: Skip hyper-slab and file appending at the moment"
    
	elif [[ ${model} == "AWI-CM-1-1-MR" ]] ; then
          echo "Re-gridding required: Skip hyper-slab and file appending at the moment"
    
	elif [[ ${model} == "CESM1-CAM5-SE-HR" ]] ; then
          ncks -O -F -d nlon,"${IDX[0]}","${IDX[1]}" -F -d nlat,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "CMCC-CM2-HR4" ]] && [[ ${exp} == "hist-1950" ]]; then
          ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "CMCC-CM2-VHR4" ]] && [[ ${exp} == "hist-1950" ]] ; then
          ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "CNRM-CM6-1-HR" ]] && [[ ${exp} == "hist-1950" ]]; then
    	if [[ ${np} == "1" ]] ; then
			echo "Skip hyper-slab and just append 3 files with total size of 1.3 GB"
    	fi		
	
	elif [[ ${model} == "CNRM-CM6-1-HR" ]] && [[ ${exp} == "historical" ]]; then
        if [[ ${np} == "1" ]] ; then
		  echo "Skip hyper-slab and just append 1 files with total size of 5.04 GB"
    	fi

	elif [[ ${model} == "EC-Earth3P" ]] ; then
		  ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
  	    
	elif [[ ${model} == "EC-Earth3P-HR" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "ECMWF-IFS-HR" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "ECMWF-IFS-MR" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "GFDL-CM4" ]] ; then
		echo "AlhmedAllah2"
      		ncks -O -F -d x,"${IDX[0]}","${IDX[1]}" -F -d y,"${IDX[2]}","${IDX[3]}" $in $out
        
	elif [[ ${model} == "GFDL-ESM4" ]] ; then
	  	echo "AlhmedAllah2"
		ncks -O -F -d x,"${IDX[0]}","${IDX[1]}" -F -d y,"${IDX[2]}","${IDX[3]}" $in $out
        	
	elif [[ ${model} == "HadGEM3-GC31-HH" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "HadGEM3-GC31-HM" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "HadGEM3-GC31-MM" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "HadGEM3-GC31-MM" ]] ; then
          	ncks -O -F -d i,"${IDX[0]}","${IDX[1]}" -F -d j,"${IDX[2]}","${IDX[3]}" $in $out
    
	elif [[ ${model} == "MPI-ESM1-2-HR" ]] ; then
    		if [[ ${np} == "1" ]] ; then
		  	echo "Skip hyper-slab and just append 25 files with total size of 0.5 GB"
    		fi
	
	elif [[ ${model} == "MPI-ESM1-2-XR" ]] ; then
    		if [[ ${np} == "1" ]] ; then
		  	echo "Skip hyper-slab and just append 25 files with total size of 0.5 GB"
    		fi

	elif [[ ${model} == "E3SM-1-0" ]] ; then
       	 	ncks -O -F -d lon,"${IDX[0]}","${IDX[1]}" -F -d lat,"${IDX[2]}","${IDX[3]}" $in $out    
	
	elif [[ ${model} == "AVISO-1-0" ]] ; then
		ncks -O -F -d lon,"${IDX[0]}","${IDX[1]}" -F -d lat,"${IDX[2]}","${IDX[3]}" $in $out

	fi
	
	##Array of files to be concatendated
	infiles+=($file)
	

	#Special case: Corret for a model with missing data
	if [[ ${period} == "200801-200812" ]] && [[ ${model_exp_sim} == "HadGEM3-GC31-HM_hist-1950_r1i2p1f1" ]] ; then
		dfile="zos_Omon_HadGEM3-GC31-HM_hist-1950_r1i2p1f1_gn_200801-200812dummy.nc"
		infiles+=($dfile)
		echo "Correct for 6 month missing data in 2008 of the NERC HadGEM3-GC31-HM_hist-1950_r1i2p1f1"
	fi

done


#[3]Concatenate for total period

#(1) Output file
output="/home/aelshall/NCO/FLmap/zos/${folder}/data/${model_exp_sim}.nc"
echo "Concatenate files"

#(2) cd to input files location
if [[ ${Hyper_slab_1D} == "indexing" ]] || [[ ${Hyper_slab_1D} == "CMIP6" ]]; then
	cd ${pathout} 

	#Skip hyper-slabing
	elif [[ ${Hyper_slab_1D} == "Unknown" ]]; then
		cd Gmap/zos/$model/$exp
fi

#(3) cat file
if [[ ${model_exp_sim} == "CESM1-CAM5-SE-HR_hist-1950_r1i1p1f1" ]] ; then
	echo "Hyper-slab time dim"
	ncks -O -F -d time,481,780 $file ${output}

elif [[ ${model_exp_sim} == "CNRM-CM6-1-HR_historical_r1i1p1f2" ]] ; then
	echo "Hyper-slab time dim"
	ncks -O -F -d time,1681,1980 $file ${output}

else
	ncrcat -O "${infiles[@]}" "${output}"
fi

#(4) Clean start
cd "/home/aelshall/NCO"
unset list
unset infiles

