Official Docker Image: https://hub.docker.com/_/mongo

```
docker run --name mongodb -p 27017:27017 -d mongo:latest
```
By default Mongo's configuration requires no authentication for access, even for the administrative user.


Mongo Express UI: https://hub.docker.com/_/mongo-express (docs is not aligned, use the command below!)

```
docker run -d --network host -e ME_CONFIG_MONGODB_URL=mongodb://localhost:27017 -e ME_CONFIG_BASICAUTH_USERNAME="user" -e ME_CONFIG_BASICAUTH_PASSWORD="password"  -p 8081:8081 mongo-express
```
Go to http://localhost:8081/