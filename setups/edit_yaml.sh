#! bin/bash

exp_name=
lon=
lat=
dep=
start_t=
end_t=

template_file=gotm_template.yaml

base_file=./${exp_name}_input/gotm.yaml
cp ${template_file} ${base_file}

sed -i "s/.*file: t_prof_file.dat.*/   file: ${exp_name}_thetao.dat/" ${base_file}
sed -i "s/.*file: s_prof_file.dat.*/   file: ${exp_name}_so.dat/" ${base_file}
sed -i "s/.*file: meteo_file.dat.*/      file: ${exp_name}_meteo.dat/" ${base_file}
sed -i "s/.*file: sst_file.dat.*/      file: ${exp_name}_sst.dat/" ${base_file}
sed -i "s/.*file: uv_avg_file.dat*/         file: ${exp_name}_uv_avg.dat/" ${base_file}
sed -i "s/.*file: zeta_file.dat*/      file: ${exp_name}_zeta.dat/" ${base_file}
sed -i "s/.*  start:.*/   start: ${start_t}/" ${base_file}
sed -i "s/.*  stop:.*/   stop: ${end_t}/" ${base_file}
sed -i "s/.*latitude:.*/   latitude: ${lat}/" ${base_file}
sed -i "s/.*longitude:.*/   longitude: ${lon}/" ${base_file}
sed -i "s/.* depth:.*/   depth: ${dep}/" ${base_file}
sed -i "s/.*name: template.*/   name: ${exp_name}/" ${base_file}
sed -i "s/.*output_filename:.*/   ${exp_name}:/" ${base_file}

