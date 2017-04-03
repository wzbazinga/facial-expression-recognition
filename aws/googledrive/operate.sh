python downloadData.py
mv fer2013+.tar.gz ../
cd ..
tar zxvf fer2013+.tar.gz
mkdir fer2013+
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
mv *.csv *.sh *.py *.xml fer2013+/
cd fer2013+
sudo chmod a+x csv2lmdb.sh
dos2unix csv2lmdb.sh
./csv2lmdb.sh