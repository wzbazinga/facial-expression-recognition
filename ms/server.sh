# this script deals with the expanding log file problem for mongodb
# run ps -aux | grep mongodb to get pid first
# then put this script under /var/lib/mongodb
while : ;
do
sudo kill -SIGUSR1 1501
sudo rm mongodb.log.2*
echo "deleted"
sleep 5s
done