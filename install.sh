#!/bin/bash

echo "installing sf501r python library ..."
mkdir temp
cd temp
echo "Downloading pigpio library ..."
wget https://github.com/joan2937/pigpio/archive/master.zip
echo "unziping pigpio sources ..."
unzip master.zip > /dev/null 2>&1
cd pigpio-master
echo "compiling pigpio master ... (this can take time : ~ 3 minutes)"
make
echo "installing pigpio library ..."
sh -c "sudo make install"
echo "everything done !"
