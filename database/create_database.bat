docker pull cassandra:4.0
docker run --name cassandra_weather_project -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:4.0
docker exec -it cassandra_weather_project bash
cqlsh
create keyspace "weather_project" with replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} and durable_writes = 'true';

sudo apt install docker.io
sudo usermod -aG docker pi
docker version
sudo nano /etc/docker/daemon.json
{
"experimental": true
}
sudo service docker stop
sudo dockerd --experimental

sudo systemctl restart docker

sudo docker pull --platform linux/amd64 cassandra:4.0

docker pull mcfongtw/rpi-cassandra:3.0

docker run --name cassandra_weather_project -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:4.0
docker run --name cwp -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d mcfongtw/rpi-cassandra:3.0
docker exec -it cassandra_weather_project bash
cqlsh
create keyspace "weather_project" with replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} and durable_writes = 'true';

sudo apt-get update && sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi
