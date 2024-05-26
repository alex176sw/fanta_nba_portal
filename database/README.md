# FantaNBA MongoDB database 
The database of the application is based on: Official Docker Image: https://hub.docker.com/_/mongo
There're two databases: the main database and the backup database.

/Execute the container:
```
docker run --name mongodb -p 27017:27017 -d -e MONGO_INITDB_ROOT_USERNAME=mongodb-user -e MONGO_INITDB_ROOT_PASSWORD=m0ng0d8 mongo:4
```

Mongo Express UI: https://hub.docker.com/_/mongo-express
```
docker run -d --network host -e ME_CONFIG_MONGODB_URL=mongodb://localhost:27017 -e ME_CONFIG_BASICAUTH_USERNAME="mongodb-user" -e ME_CONFIG_BASICAUTH_PASSWORD="m0ng0d8"  -p 8081:8081 mongo-express
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






