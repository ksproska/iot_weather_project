docker pull cassandra:4.0
docker run --name cassandra_weather_project -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:4.0

docker ps
docker exec -it cassandra_weather_project
docker exec -it cassandra_weather_project bash
