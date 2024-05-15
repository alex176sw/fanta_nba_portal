FROM node:21 
WORKDIR /app
RUN apt-get update && apt-get install -y vim curl

COPY . .
COPY package*.json ./
COPY ./entrypoint.sh /
RUN npm install

EXPOSE 3000
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]