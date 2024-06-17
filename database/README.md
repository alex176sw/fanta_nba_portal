# FantaNBA MongoDB databases 
The databases of the application are based on: Official Docker Image: https://hub.docker.com/_/mongo
There're three databases: the data database, the data_backup database and the ML database.

Execute the container:
```
docker network create mldatabase-network
docker network create mongodb-network


docker run --network mongodb-network --name mongodb -p 27017:27017 -d -e MONGO_INITDB_ROOT_USERNAME=mongodb-user -e MONGO_INITDB_ROOT_PASSWORD=m0ng0d8 mongo:4

docker run --network mldatabase-network --name mldatabase -p 27017:27017 -d -e MONGO_INITDB_ROOT_USERNAME=mongodb-user -e MONGO_INITDB_ROOT_PASSWORD=m0ng0d8 mongo:4
```

Mongo Express UI: https://hub.docker.com/_/mongo-express
```
docker run --network host -e ME_CONFIG_MONGODB_URL=mongodb://mongodb:27017 -e ME_CONFIG_BASICAUTH_USERNAME="mongodb-user" -e ME_CONFIG_BASICAUTH_PASSWORD="m0ng0d8"  -p 8081:8081 mongo-express

docker run --network mldatabase-network -e ME_CONFIG_MONGODB_URL=mongodb://mongodb-user:m0ng0d8@mldatabase:27017 -e ME_CONFIG_BASICAUTH_USERNAME="mongodb-user" -e ME_CONFIG_BASICAUTH_PASSWORD="m0ng0d8"  -p 8081:8081 mongo-express
```
Go to http://localhost:8081/

# FantaNBA Synchdb service
This micro-service synchronize the main database with the backup database.

## Instructions
To build and push the Docker container:
```
docker build -t alex176/azure-dbsynch-service:v1.2 .
docker push alex176/azure-dbsynch-service:v1.2
```

Execute the container:
```
docker container run --name dbsynch -d --network host alex176/azure-dbsynch-service:v1.2
```






