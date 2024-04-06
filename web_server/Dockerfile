FROM node:21 
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]