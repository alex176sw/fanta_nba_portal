# FantaNBA Front-end
The front-end of the application. It's a web server that provides a REST API and it's implemented with NodeJs.

## Instructions
To build and push the Docker container:
```
docker build -t alex176/azure-scalable-app-prototype-frontend:v1.2 .
docker push alex176/azure-scalable-app-prototype-frontend:v1.2
```
To run the container:
```
docker container run --name nodejs-app-frontend -d --network host -p 3000:3000 alex176/azure-scalable-app-prototype-frontend:v1.2
```

To develop use: https://github.com/nodejs/docker-node/blob/main/README.md#how-to-use-this-image
```
docker run -it --network host --rm --name node-app-dev -p 3000:3000 -v "$PWD":/usr/src/app -w /usr/src/app node:21 bash -l

# Initialization
npm init
npm install express --save

# Starting the app
node app/index.js
```
