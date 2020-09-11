cat ./bin/dockerPW.txt | sudo docker login --username dicotiar --password-stdin
sudo docker build -t youtora_fe ./
sudo docker push dicotiar/youtora_fe
