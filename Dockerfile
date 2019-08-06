# start with a base simple os
FROM alpine

# establish the working directory in the container
WORKDIR /home/application

# run the alpine package manager to install node and npm
RUN apk add --update nodejs npm

# copy the package.json to the container
COPY ./package.json ./

# install dependencies
RUN npm install

# notice the location of this file
# it's towards the end so a change in this file does not cause a lengthy rebuild
COPY ./app.js ./

# the default command, run from the working directory inside the container
CMD ["npm", "start"]

