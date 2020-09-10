#!/bin/bash
docker stop youtora_fe

echo final port will be 11000
echo enter host name:

# shellcheck disable=SC2162
read host_name

docker build -t youtora_fe ./

if [ ${#hostname} == 0]
then
	docker run --rm -d -it -h "johnjongyoonkim.com" -p 11000:80 --name youtora_fe youtora_fe
else
	docker run --rm -d -it -h "$host_name" -p 11000:80 --name youtora_fe youtora_fe
fi
exit 0
