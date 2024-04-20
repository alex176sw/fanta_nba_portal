Node.js Docker Image: https://github.com/nodejs/docker-node/blob/main/README.md#how-to-use-this-image

To initialize a Node.js project:
``` 
docker run -it --rm --name my-node -v "$PWD":/usr/src/app -w /usr/src/app node:21 bash -l
npm init
npm install express --save
```

To build and run the Docker container:
```
docker build -t alex176/azure-scalable-app-prototype-frontend:v1 .
docker container run -p 3000:3000 alex176/azure-scalable-app-prototype-frontend:v1
```

To push the image:
```
docker push alex176/azure-scalable-app-prototype-frontend:v1
```


