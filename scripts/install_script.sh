#!/bin/bash

CPU="$(nproc)"

echo "Cloning FABM"
git clone https://github.com/fabm-model/fabm.git

echo "Cloning ERSEM"
git clone https://github.com/mikebedington/ersem_windfarm.git

echo "Cloning GOTM"
git clone https://github.com/mikebedington/gotm_windfarm.git
cd gotm

git submodule update --init --recursive
#cd ../
#cd gotm && git checkout v5.3 && git submodule update --init --recursive && cd ..
cd ../

echo "Cloning model setup"
git clone https://github.com/mikebedington/model_windfarm.git

echo "Building GOTM-FABM"

mkdir install
mkdir build && cd build

cmake ../gotm -DFABM_BASE=../fabm -DFABM_ERSEM_BASE=../ersem -DCMAKE_INSTALL_PREFIX=../install -DGOTM_USE_SEAGRASS=ON

make install -j $CPU

cd ../

# Run test setup


# Enable fabm in gotm.yaml and add absorption_of_silt and mole_fraction_of_carbon_dioxide_in_air
../install/bin/gotm



