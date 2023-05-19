FROM node:14 as build 

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .



EXPOSE 3000

CMD ["npm", "run", "dev"]