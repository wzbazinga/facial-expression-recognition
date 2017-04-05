# this script running in aws Deep Learning AMI Ubuntu Linux - 1.2 (ami-e9038d89)

# config path for caffe
echo PATH=/home/ubuntu/src/caffe/build/tools/:$PATH >> ~/.bashrc
source ~/.bashrc

# install needed software
sudo apt update;
sudo apt install git;

# '\r' in shell script lead to error
# dos2unix is used to remove the  '\r' character in shell script
sudo apt install dos2unix;

# install ftp server
sudo apt install vsftpd;
sudo chmod a+w /etc/vsftpd.conf
echo -e "userlist_deny=NO\nuserlist_enable=YES\nuserlist_file=/etc/allowed_users\nseccomp_sandbox=NO\nwrite_enable=YES" >> /etc/vsftpd.conf
sudo touch /etc/allowed_users
sudo chmod a+w /etc/allowed_users
sudo echo ubuntu >> /etc/allowed_users
sudo service vsftpd restart

sudo pip install imutils;
sudo pip install pyDrive;

# prepare work dir
sudo mkdir snapshot
sudo chmod 777 snapshot

# install nvidia digits
CUDA_REPO_PKG=cuda-repo-ubuntu1404_7.5-18_amd64.deb &&
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/$CUDA_REPO_PKG &&
sudo dpkg -i $CUDA_REPO_PKG
sudo apt update
sudo apt install digits
sudo pip install setuptools==33.1.1

# set user password
sudo passwd ubuntu
