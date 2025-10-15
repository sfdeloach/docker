# Docker and Kubernetes: The Complete Guide

Course notes from Stephen Grider's lectures on Udemy.com

## contents

- [Docker and Kubernetes: The Complete Guide](#docker-and-kubernetes-the-complete-guide)
  - [contents](#contents)
  - [definitions](#definitions)
  - [basics with the CLI](#basics-with-the-cli)
  - [custom images](#custom-images)
  - [making real projects (Section 04)](#making-real-projects-section-04)
  - [docker compose - multiple containers (Section 05)](#docker-compose---multiple-containers-section-05)
  - [creating a production grade workflow (Section 06)](#creating-a-production-grade-workflow-section-06)
    - [course material](#course-material)
      - [tests](#tests)
      - [build and run](#build-and-run)
    - [another example](#another-example)

## definitions

- **image:** A read-only template that contains all the necessary components—such as application code, runtime, system tools, libraries, and settings—to run a software application within a container. Think of it as a cookie cutter.
- **container:** A lightweight, standalone, executable package that includes everything needed to run an application, such as the code, runtime, system tools, libraries, and configuration files. An instance of an image. Think cookie.

## basics with the CLI

```bash
  $ docker run hello-world            # verify installation
  $ docker version                    # info
  $ docker run <image>                # create & run container from an image, download if needed
  $ docker run <image> <command>      # override the default image command
  $ docker run busybox echo "hello"   # example
  $ docker ps                         # list running containers
  $ docker container ls               # same as `docker ps`
  $ docker ps -a                      # list all containers
  $ docker create <image>             # step 1: create a new image
  $ docker start <container>          # step 2: start new instance from image
  $ docker run <image>                # combines steps 1 & 2
  $ docker start -a <container>       # start and attach to a stopped container
  $ docker run -it <image> sh         # create, start, and attach w/ sh console shell
  $ docker run -it ubuntu bash        # create, start, attach to a ubuntu bash console shell
  $ docker exec -it <container> <cmd> # attach to a running container with command
  $ docker exec -it <container> bash  # example command prompt in a running container
  $ docker stop <container>           # stop container via SIGTERM (preferred)
  $ docker kill <container>           # kill container via SIGKILL
  $ docker system prune               # deletes stopped containers
  $ docker logs <container>           # view console output
  $ docker image ls                   # view downloaded/created local images
  $ docker images                     # same as `docker image ls`
```

## custom images

Custom images are built with a `Dockerfile`:

```Dockerfile
# Use an existing docker image as a base
FROM alpine

# Download and install a dependency
RUN apk add --update redis

# Tell the image what command to run when it starts
CMD ["redis-server"]
```

Building the image (command executed from the same directory as `Dockerfile`). Docker will cache dependencies for faster rebuilds. By convention, the tag is prefixed with your Docker ID:

```bash
  $ docker build .
  $ docker build -t sfdeloach/redis:latest . # tag images with name and version
```

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

## making real projects (Section 04)

See `Dockerfile` in `04-simple-server` for an example of how to build a nodeJS express server image using a Dockerfile. Take notice of the following:

- specify a tag with a base image for specificity
- set a working directory inside your container, `/usr/src/app` is a conventional location for most containerized applications
- copy build files from your local machine into your container
- map network ports to your container during the `run` or `create` command
- put thought into the order of commands in the Dockerfile to minimize rebuild times

**NOTE:** While it is possible to place multiple services inside a container, however, this is not good practice. Each service should be placed in its own container so that there is greater flexibility when scaling.

## docker compose - multiple containers (Section 05)

Up to this point, we have used the Docker CLI to work with containers. As projects grow, this becomes clunky. [Docker Compose](https://docs.docker.com/compose/) is used in industry to manage complexity. Docker Compose defines and runs multi-container applications and streamlines the development and deployment experience.

Docker Compose sets up a single network for your application(s) by default, adding each container for a service to the default network. Containers on a single network can reach and discover every other container on the network. External connections must be explicitly defined.

A `compose.yml` is used by Docker Compose to create containers.

The contents of a simple `compose.yml` file:

```yml
# services define a resource that can be scaled and managed independently
services:
  # first container, this name becomes its discoverable hostname on the default network
  redis-server:
    # image available on docker hub
    image: "redis:8.2-alpine"
  # second container w/ host name 'node-app'
  node-app:
    # restart policies include "no" (default), always, on-failure, and unless-stopped
    restart: always
    # looks for the Dockerfile to build this image
    build: .
    # must explicitly define a port if external connection desired
    ports:
      # maps port 80 on the local machine to port 3000 in the container instance
      - "80:3000"
```

```bash
  $ docker compose up         # create and start containers
  $ docker-compose up -d      # detached mode, run in background
  $ docker-compose up --build # build images before starting
  $ docker compose ps         # list containers
  $ docker compose stop       # stop services
  $ docker compose start      # start services
  $ docker compose down       # stop and remove containers
```

See two examples of multi-container applications in `05-docker-compose`:

- A simple redis backend and express js api
- A slightly more complicated postgres db, adminer db manager, and fastAPI api

When working with volumes, some helpful commands include:

```bash
 $ docker volume ls          # list volumes
 $ docker volume prune       # remove unused local volumes
 $ docker volume rm <volume> # remove one or more volumes
```

## creating a production grade workflow (Section 06)

### course material

The workflow is a cycle:

![workflow cycle diagram](./images/01-workflow-cycle.png)

In this section, the workflow will look like this:

![flow specifics](./images/02-flow-specifics.png)

Create a new react app, run the out of the box test, and build the application to make sure the application works:

```bash
  $ create-react-app my-app
  $ cd my-app
  $ npm start
  $ npm run test
  $ npm run build
```

Note that the preceding commands created the `node_modules` directory, which will contain a significant number of directories and files. For the purpose of demonstrating docker volumes in a later step, remove the `node_modules` directory:

```bash
  $ rm -rf node_modules
```

Remaining in the `frontend` directory, create a development Dockerfile:

```bash
  $ touch Dockerfile.dev
```

This file will use the `npm run start` command during development. Later we will create the conventional `Dockerfile` that will use the `npm run build` command for production. The contents of the `Dockerfile.dev` will provide the setup of our development container:

```Dockerfile
## Dockerfile.dev
FROM node:lts-alpine3.22

# Set working directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

# Start development server
CMD ["npm", "start"]
```

Running `docker build .` will look for the default `Dockerfile`, which does not exist at this time. The build file must be explicitly defined using the `-f` flag:

```bash
  $ docker build -t sfdeloach/react-dev:latest -f Dockerfile.dev .
```

Options added to the run command allow bookmarks and mappings to a volume. This will allow the react development server the ability to detect changes made locally. Notice that both bookmarks and mappings use the same `-v` flag. The only difference is the colon, which is a similar syntax used earlier to map a local port to a container's port:

```bash
  $ docker run -p 3000:3000 -v usr/src/app/node_modules -v $(pwd):/usr/src/app <image>
  $ ######################## ^ bookmark ################ ^ mapping ###################
```

This example is purposefully designed to demonstrate the use of bookmarks and volumes. In this example, we deleted the `node_modules` directory locally, which contained scripts needed to start our development environment. Mapping the contents of our local working directory will not provide it since it no longer exists. However, recall that the command `npm install` was run on our container during the build. This installed a copy of `node_modules` in the container. The bookmark tells the container to look inside its own file system for any references to the `node_modules` directory. This bookmark is intentionally place before the mapping.

As an aside, a simpler development container could be created. Only the `package.json` file would be needed to run the initial npm script and only a mapping to the working directory is needed if `node_modules` was not removed:

```Dockerfile
FROM node:lts-alpine3.22
WORKDIR '/usr/src/app'
COPY package.json .
CMD ["npm", "start"]
```

Build the image as shown above, then run with only the mapping:

```bash
  $ docker run -p 3000:3000 -v $(pwd):/usr/src/app <image>
```

The container would be able find `node_modules` on the local machine using this approach. Returning to the contrived example that uses a bookmark for the `node_modules` directory, the run command is rather lengthy. [Docker Compose](https://docs.docker.com/compose) to the rescue!

```bash
  $ touch compose.yml
```

The contents of `compose.yml`:

```yml
services:
  web:
    build:
      # sets the directory to the current folder
      context: .
      # unconventional name, must be explicitly defined
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      # bookmark, look inside the container, no ":" is used
      - /usr/src/app/node_modules
      # mapping local directory to the container's /app directory
      - .:/usr/src/app
```

#### tests

To run tests, override the run command as demonstrated before:

```bash
  $ docker run -it <image> npm run test
```

Running the command as demonstrated above causes a small problem. A new container is created with its own filesystem, therefore, it is unable to detect any live changes to the source. There are two solutions, each with advantages and disadvantages. The first solution uses the `exec` command on the running running container:

```bash
  $ docker exec -it <container> npm run test
```

The drawback on this approach requires a second step and keeping the container ID in mind. The second solution is to setup an additional service in `compose.yml`:

```yml
...
(append the service 'tests' to existing file...)
...

tests:
    build:
      context: .
      dockerfile: Dockerfile.dev
    # Override the default command to run tests
    volumes:
      - /usr/src/app/node_modules
      - .:/usr/src/app
    command: ["npm", "run", "test"]
```

The test results update as expected and they are conveniently started in its own container, however, the terminal is not attached to the standard input, which does not allow for an interactive experience. Consider which option may be best for your current testing objectives.

#### build and run

To this point in the exercise, we have setup a development and testing container. Now it is time to move to production. This will be accomplished in a multi-step build process. In this case it will occur in one `Dockerfile` that specifies two phases: **BUILD** and **RUN**

The _build phase_ will use `node:lts-alpine3.22` as a base image and install all dependencies in order to build the react app.

The _run phase_ will use `nginx` as a base image, copy over the results of the _build phase_ and start the Nginx server.

The multi phase `Dockerfile`:

```Dockerfile
# Multi-stage Dockerfile for Production
FROM node:lts-alpine3.22 AS build

# Set working directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

# Build the app
RUN npm run build

# Produce a lean production image
FROM nginx:1.29.2-alpine

# Copy built app from the build stage
COPY --from=build /usr/src/app/build /usr/share/nginx/html
```

Note the following:

- it is not necessary to install all the dev dependencies in our production container
- in fact, node is not needed at all in production, we are only serving static content
- build stages can be named to increase readability: `FROM node:lts-alpine3.22 AS builder`
- no `RUN` command is necessary for nginx, the server is enabled by default

We are now ready to build our production image and run it:

```bash
  $ docker build -t sfdeloach/nginx-server:latest .
  $ docker run -p 8080:80 <image>
```

### another example

The following is an example that builds on the course's example. Concepts include:

1. Using [Vite](vite.dev) to build a simple frontend.
2. Setting up a development container that provides live updates.
3. Setting up a testing container from the development image for live updates.
4. Using volumes efficiently between local and container environments.
5. Setting up a production container via multi-step builds using Nginx server
