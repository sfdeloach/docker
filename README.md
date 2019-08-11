# Docker and Kubernetes: The Complete Guide
Course notes from Stephen Grider's lectures on Udemy.com

## Contents
1. [Dive into Docker](#dive-into-docker)
2. [Manipulating Containers with the Docker Client](manipulating-containers-with-the-docker-client)

## Dive into Docker
**image**
> Containers are created from images. Think cookie cutter.

**container**
> An instance of an image. Think cookie.

## Manipulating Containers with the Docker Client

Verify installation:  
```bash
  $ docker run hello-world
```

Info on installation:  
```bash
  $ docker version
```

Create and run a new container from image:  
```bash
  $ docker run <image name>
```
> If the image is not already loaded then it will pull the image from the repo before it starts

Default command override:  
```bash
  $ docker run <image name> command
```

For example this prints "hi there" to terminal:  
```bash
  $ docker run busybox echo "hi there" 
```

List of running containers:  
```bash
  $ docker ps
```
> Alias for `docker container ls`. By default, only running containers in the local repo are listed.

List of all containers, running and stopped:  
```bash
  $ docker ps -a
```
> The `-a` flag is short for `--all`. See `man docker container-ls` for more info.

The run command combines the create and start commands:  
```bash
  $ docker run <image name>
  $ # same as
  $ docker create <image name> && docker start <container id>
```

Creates a new container from an image:  
```bash
  $ docker create <image name>
```

Starts the specified container, echos the id:  
```bash
  $ docker start <container id>
```

The `-a` flag attaches to the running container:  
```bash
  $ docker start -a <container id>
```
> A container can be restarted using the start command combined with the target container id  

Remove stopped containers:  
```bash
  $ docker system prune
```

Get logs from a container:  
```bash
  $ docker logs <container id>
```

Stop a container (SIGTERM):  
```bash
  $ docker stop <container id>
```
> If unsuccessful after 10 seconds, this command will revert to the kill command

Kill a container (SIGKILL):  
```bash
  $ docker kill <container id>
```
> Does not allow the container to gracefully shutdown, `stop` command is preferred

Execute a command in a running container:  
```bash
  $ docker exec -it <container id> <command>
```
> Run a command in a running container. The `-i` keeps STDIN open and will make the session
interactive. The `-t` flag will allocate a pseudo-TTY and make the session prettier.  

Get a command prompt in a container:  
```bash
  $ docker exec -it <container id> bash
```
> Provides interactive bash shell on a running container.

Run (create & start) a new container and bring up an interactive shell:  
```bash
  $ docker run -it <image name> sh
```

Run a new Ubuntu container and start bash shell:
```bash
  $ docker run -it ubuntu bash
```
> Docker containers run on isolated filesystems.

View docker images on your local machine:  
```bash
  $ docker image ls
  $ # or
  $ docker images
```

## Building Custom Images Through Docker Server

Custom images are built with a `Dockerfile`:  

```Dockerfile
# Use an existing docker image as a base
FROM alpine

# Download and install a dependency
RUN apk add --update redis

# Tell the image what command to run when it starts
CMD ["redis-server"]
```

Building the image (command executed from the same directory as `Dockerfile`):  
```bash
  $ docker build .
```  
> Docker will cache dependencies for faster rebuilds

Build an image with repository info, name, and tag (version):  
```bash
  $ docker build -t sfdeloach/redis:latest .
```  
> By convention, the tag is prefixed with your Docker ID

Another (nonsensical) example:  

```Dockerfile
# Use an existing image of Fedora
FROM fedora

# Download nodejs and gcc with its package manager
RUN dnf update -y
RUN dnf install -y nodejs
RUN dnf install -y gcc

# Run ping when the container starts, notice the string array format
CMD ["ping","archlinux.org"]
```

## Making Real Projects with Docker

See `Dockerfile` in `04-simple server` for an example of how to build a nodeJS express server image
using a Dockerfile. Take notice of the following:

- specify a tag with a base for more images
- set a working directory inside your container
- copy build files from your local machine into your container
- map network ports to you container
- put thought into the order of commands in the Dockerfile to minimize rebuild times

## Docker Compose with Multiple Local Containers

It is possible to place multiple services inside a container, however, this is not good practice.
Each service should be placed in its own container so that there is greater flexibility when
scaling.

Docker Compose sets up a single network for your application(s) by default, adding each container 
for a service to the default network. Containers on a single network can reach and discover every
other container on the network.

A `docker-compose.yml` is used by Docker Compose to create containers.
```
  $ touch docker-compose.yml
```

The contents of `docker-compose.yml`:
```
version: '3'
services:
  redis-server:
    image: 'redis'
  node-app:
    restart: always
    build: .
    ports:
      - "80:3000"

# restart policies include "no" (default), always, on-failure, and unless stopped
```

The containers are built by running the command:
```bash
docker-compose up --build --project-name visits
```

To see a list of running containers created by Docker Compose, be sure you are in the project
folder and run:
```bash
docker-compose ps
```

To launch containers in the background:
```bash
docker-compose up -d
```

To stop containers created by Docker Compose:
```bash
docker-compose down
```

## Creating a Production-Grade Workflow

The workflow is a cycle:
```
       ┌<--------------------------------------┐
       │                                       │
       └-->Development-->Testing-->Deployment->┘
```

In this example, found in `06-production-workflow`, the specific workflow will look like this:
```
       ┌----------------------------------┐
       │           Github Repo            │ 
       └----------------------------------┘
       feature --- pull request ---> master ---> Travis CI ---> Deploy
        branch                       branch      (testing)      to AWS
          ^                                                       │
          │                                                       │
          │                                                       │
   Develop Locally <----------------------------------------------┘
```

Install dependencies for node, npm, and react, if not already installed on your local machine:
```
  $ # Fedora package manager
  $ dnf install node npm
  $ npm install -g create-react-app
```

Create a new react app, run the out of the box test, and build the application to make sure the
application works. Note that these steps will create the `node_modules` directory, which will
contain a significant number of directories and files. In a later step, this directory will be
removed in order to prevent unnecessary duplication:
```
  $ create-react-app frontend
  $ cd frontend
  $ npm start
  $ npm run test
  $ npm run build
```

Remaining in the `frontend` directory, create a development Dockerfile:
```
  $ touch Dockerfile.dev
```

This file will use the `npm run start` command during development. Later we will create the 
conventional `Dockerfile` that will use the `npm run build` command for production.

The contents of the `Dockerfile.dev` will provide the setup of our development container:
```
FROM node:alpine

WORKDIR '/app'

COPY package.json .
RUN npm install

# Be sure to delete the local node_modules directory if this "shortcut" copy command is used
COPY . .

# Instead of deleting the local node_modules directory, files could be explicity copied instead

CMD ["npm","run","start"]
```

Running `docker build .` will look for the default `Dockerfile`, which does not exist at this time.
The build file must be explicitly defined using the `-f` flag:
```
  $ docker build -t sfdeloach/react-dev -f Dockerfile.dev .
```

Options added to the run command allow bookmarks and mappings to a volume. This will allow the
react development server the ability to detect changes made locally. Notice that both bookmarks
and mappings use the same `-v` flag. The only difference is the colon, which is a similar syntax
used earlier to map a container's port to the local machine's port:
```bash
 $ docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image id>
 $ #                       ^this is a bookmark  ^this is a mapping
```

The above run command is rather lengthy. Docker Compose to the rescue!
```
  $ touch docker-compose.yml
```

The contents of `docker-compose.yml`:
```
version: '3'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app

# The context allows a reference to a different directory
#   if the current directory is not the working directory.
```

To run tests, override the run command as demonstrated before:
```
  $ docker run -it <image id> npm run test
```

Running the command as demonstrated above causes a small problem. A new container is created with
its own filesystem, therefore, it is unable to detect any live changes to the source. There are
two solutions. The first solution uses the `exec` command on the running running container:
```
  $ docker exec -it <image id> npm run test
```

The second solution is to setup an additional service in `docker-compose.yml`:
```
...(append this to the bottom of the existing file)...

  tests:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - /app/node_modules
      - .:/app
    command: ["npm","run","test"]
```

There is a drawback with this approach. The test results update as expected, however, the terminal
is not attached and does not allow for an interactive experience.


