docker pull cassandra:4.0
docker run --name cassandra_weather_project -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:4.0
docker exec -it cassandra_weather_project bash
cqlsh
create keyspace "weather_project" with replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} and durable_writes = 'true';
