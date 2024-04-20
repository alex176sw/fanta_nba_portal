FROM node:21 
WORKDIR /app
COPY . .
COPY package*.json ./
COPY ./entrypoint.sh /
RUN npm install

EXPOSE 3000
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]