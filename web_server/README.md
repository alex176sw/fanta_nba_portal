https://github.com/nodejs/docker-node/blob/main/README.md#how-to-use-this-image
docker run -it --rm --name my-node -v "$PWD":/usr/src/app -w /usr/src/app node:21 bash -l
npm init
npm install express --save

docker build -t node-web-server:v1 .
docker container run -p 5000:5000 node-web-server:v1 500
