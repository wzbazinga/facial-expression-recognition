# get training images
rm -rf pic
mkdir pic
rm train.txt validate.txt test.txt
python csv2img.py

# convert images to lmdb
rm -rf train validate test
convert_imageset --shuffle --check_size --gray ./ train.txt train
convert_imageset --shuffle --check_size --gray ./ validate.txt validate
convert_imageset --shuffle --check_size --gray ./ test.txt test

# compute the mean value of each pixel
rm train.binaryproto
compute_image_mean train train.binaryproto
#compute_image_mean validate validate.binaryproto
#compute_image_mean test test.binaryproto

# convert .binaryproto to .npy (optional)
rm train.npy
python bin2npy.py train.binaryproto train.npy
#python bin2npy.py validate.binaryproto validate.npy
#python bin2npy.py test.binaryproto test.npy

# start caffe training process
cd ..
caffe train -solver solver.prototxt