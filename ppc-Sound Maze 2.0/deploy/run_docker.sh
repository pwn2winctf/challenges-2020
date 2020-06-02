#sudo docker rm -vf $(sudo docker ps -a -q)
#sudo docker rmi -f $(sudo docker images -a -q)
sudo docker build -t sm .
sudo docker run -d -p 31337:31337 --name sound_maze sm
