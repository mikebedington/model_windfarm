#!/bin/bash

CPU="$(nproc)"

echo "Cloning FABM"
git clone https://github.com/fabm-model/fabm.git

echo "Cloning ERSEM"
git clone https://github.com/pmlmodelling/ersem.git

echo "Cloning GOTM"
git clone https://github.com/gotm-model/code.git gotm
cd gotm

git submodule update --init --recursive
#cd ../
#cd gotm && git checkout v5.3 && git submodule update --init --recursive && cd ..
cd ../

echo "Cloning GOTM examples"
git clone https://github.com/gotm-model/cases.git

echo "Cloning ERSEM examples"
git clone https://github.com/pmlmodelling/ersem-setups.git

echo "Cloning Lena 1D model"
git clone https://github.com/riquitorres/Lena-1D.git

echo "Building GOTM-FABM"

mkdir install
mkdir build && cd build

cmake ../gotm -DFABM_BASE=../fabm -DFABM_ERSEM_BASE=../ersem -DCMAKE_INSTALL_PREFIX=../install -DGOTM_USE_SEAGRASS=ON

make install -j $CPU

cd ../

# Run test

# We want to try the seagrass model, need to convert the xml to yaml
mkdir testing

cp cases/nns_annual/* testing/
cp ersem-setups/L4/fabm.yaml testing/
cp /home/michael/Projects/Svalbard/models/gotm_with_nutrients/run_loop.sh testing/
cp /home/michael/Projects/Winfarm_carbon/Models/gotm_seagrass/nsea_seagrass/seagrass* testing/ 
cd testing

# Enable fabm in gotm.yaml and add absorption_of_silt and mole_fraction_of_carbon_dioxide_in_air
../install/bin/gotm



