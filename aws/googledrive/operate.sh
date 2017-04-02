python downloadData.py
mv fer2013+.tar.gz ../
cd ..
tar zxvf fer2013+.tar.gz
mkdir fer2013+
mv *.csv *.sh *.py fer2013+/
cd fer2013+
sudo chmod a+x csv2lmdb.sh
./csv2lmdb.sh