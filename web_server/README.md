Node.js Docker Image: https://github.com/nodejs/docker-node/blob/main/README.md#how-to-use-this-image

To develop a Node.js project:
```
docker run -it --network host --rm --name node-app-dev -p 3000:3000 -v "$PWD":/usr/src/app -w /usr/src/app node:21 bash -l

# Initialization
npm init
npm install express --save

# Starting the app
node app/index.js
```



To build and run the Docker container:
```
docker build -t alex176/azure-scalable-app-prototype-frontend:v1 .
docker container run --name nodejs-app-frontend -d --network host -p 3000:3000 alex176/azure-scalable-app-prototype-frontend:v1
```

To push the image:
```
docker push alex176/azure-scalable-app-prototype-frontend:v1
```


