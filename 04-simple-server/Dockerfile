# start with a base OS with a tag specified
FROM alpine:3.9.4

# establish the working directory in the container
WORKDIR /usr/src/app

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

# To build an image from a Dockerfile
# $ docker build -t sfdeloach/simpleserver .

# To map a local port to a container port:
# $ docker run -p 80:3000 <image id>
# or
# $ docker create -p 80:3000 <image id>
