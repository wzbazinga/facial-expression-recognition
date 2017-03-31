# config path for caffe
echo PATH=/home/ubuntu/src/caffe/build/tools/:$PATH >> ~/.bashrc
source ~/.bashrc

# install needed software
sudo apt update
sudo apt install git

sudo apt install vsftpd
sudo chmod a+w /etc/vsftpd.conf
echo -e "userlist_deny=NO\nuserlist_enable=YES\nuserlist_file=/etc/allowed_users\nseccomp_sandbox=NO\nwrite_enable=YES" >> /etc/vsftpd.conf
sudo touch /etc/allowed_users
sudo chmod a+w /etc/allowed_users
sudo echo ubuntu >> /etc/allowed_users
sudo service vsftpd restart

sudo pip install pyDrive

# prepare work dir
sudo mkdir snapshot
sudo chmod 777 snapshot

sudo passwd ubuntu
