#!/bin/bash
sudo python getlabeltxt.py

rm -rf train validate test
convert_imageset --check_size --gray --shuffle ./ train.txt train
convert_imageset --check_size --gray --shuffle ./ validate.txt validate
convert_imageset --check_size --gray --shuffle ./ test.txt test

compute_image_mean train train.binaryproto
#compute_image_mean validate validate.binaryproto
#compute_image_mean test test.binaryproto

python binary2npy.py train.binaryproto train.npy
#python binary2npy.py validate.binaryproto validate.npy
