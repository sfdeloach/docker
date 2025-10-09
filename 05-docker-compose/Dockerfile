FROM alpine

WORKDIR /usr/server

RUN apk update
RUN apk upgrade
RUN apk add --update nodejs npm

COPY ./package.json ./

RUN npm install

COPY ./app.js ./

CMD ["npm","start"]
