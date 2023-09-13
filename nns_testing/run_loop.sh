#! bin/bash

experiment_name=test_nutrients_all

bin=/home/michael/Projects/Svalbard/code/install_dir/bin/gotm
output_dir=/home/michael/Projects/Svalbard/model_output/${experiment_name}
coldstart=1

START=1
END=3

mkdir -p ${output_dir}
cp *.yaml ${output_dir}
cp *.txt ${output_dir}
cp *.sh ${output_dir}

for (( i=$START; i<=$END; i++ ))
do
	if [[ "$coldstart" == "1" ]]
	then
        sed -i 's/^  load:.*$/  load: false/g' gotm.yaml
		coldstart=0
    else
		sed -i 's/^  load:.*$/  load: true/g' gotm.yaml
	fi	
	
    echo -n "Starting loop "$i
	$bin > gotm_log_${i}.txt
	io=$(printf %03d $n)
    cp restart.nc ${output_dir}/restart_${io}.nc
    mv nns_annual.nc ${output_dir}/output_${io}.nc
	ncatted -O -a units,time,o,c,"seconds since 1998-01-01 00:00:00" restart.nc
done

mv gotm_log_*.txt ${output_dir}
