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
  - [creating a production grade workflow](#creating-a-production-grade-workflow)
  - [CI/CD w/ AWS](#cicd-w-aws)

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
  $ docker exec -it <container> <cmd> # run and attach to a running container with command
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

## making real projects (Section 04)

See `Dockerfile` in `04-simple server` for an example of how to build a nodeJS express server image using a Dockerfile. Take notice of the following:

- specify a tag with a base image for specificity
- set a working directory inside your container
- copy build files from your local machine into your container
- map network ports to your container
- put thought into the order of commands in the Dockerfile to minimize rebuild times

## docker compose - multiple containers (Section 05)

TODO: CLI becomes too clunky, docker compose is used in industry to manage complexity

It is possible to place multiple services inside a container, however, this is not good practice.
Each service should be placed in its own container so that there is greater flexibility when
scaling.

Docker Compose sets up a single network for your application(s) by default, adding each container
for a service to the default network. Containers on a single network can reach and discover every
other container on the network. External connections must be explicitly defined.

A `docker-compose.yml` is used by Docker Compose to create containers.

The contents of a simple `docker-compose.yml` file:

```yml
version: "3.8"      # as of October 2025, 3.8 is latest version
services:           # services can be thought of as containers
  redis-server:     # first container, this name becomes its hostname
    image: "redis"  # image available on docker hub
  node-app:         # second container w/ host name 'node-app'
    restart: always # restart policies include "no" (default), always, on-failure, and unless stopped
    build: .        # looks for the Dockerfile to build this image
    ports:          # must explicitly define a port if external connection desired
      - "80:3000"   # maps port 80 on the local machine to port 3000 in the container instance
```

```bash
  $ docker-compose up build -p visits # build and run containers
  $ docker-compose ps 
```

To see a list of running containers created by Docker Compose, be sure you are in the project
folder and run:

```bash
```

To launch containers in the background:

```bash
  $ docker-compose up -d
```

To stop containers created by Docker Compose:

```bash
  $ docker-compose down
```

## creating a production grade workflow

The workflow is a cycle:

```
       ┌<───────────────────<─────────────────────┐
       │                                          │
       └──>Development──>Testing──>Deployment───>─┘
```

In this example, found in `06-production-workflow`, the specific workflow will look like this:

```
       ┌──────────────────────────────────┐
       │           Github Repo            │
       └──────────────────────────────────┘
       feature ───▶ pull request ───▶ master ───▶ Travis CI ───▶ Deploy
        branch                       branch      (testing)      to AWS
          ▲                                                        │
          │                                                        │
          │                                                        │
   Develop Locally <───────────────────────────────────────────────┘
```

This section and the next, [Continuous Integration and Deployment with AWS](#continuous-integration-and-deployment-with-aws),
will cover the workflow cycle in greater detail.

To begin, first install dependencies for node, npm, and react, if not already installed on your
local machine:

```bash
  $ dnf install node npm    ### Fedora package manager ###
  $ npm install -g create-react-app
```

Create a new react app, run the out of the box test, and build the application to make sure the
application works:

```bash
  $ create-react-app frontend
  $ cd frontend
  $ npm start
  $ npm run test
  $ npm run build
```

Note that the preceding commands created the `node_modules` directory, which will contain a
significant number of directories and files. For the purpose of demonstrating docker volumes in a
later step, remove the `node_modules` directory:

```bash
  $ rm -rf node_modules
```

Remaining in the `frontend` directory, create a development Dockerfile:

```bash
  $ touch Dockerfile.dev
```

This file will use the `npm run start` command during development. Later we will create the
conventional `Dockerfile` that will use the `npm run build` command for production. The contents
of the `Dockerfile.dev` will provide the setup of our development container:

```Dockerfile
(Dockerfile.dev)
FROM node:alpine

WORKDIR '/app'

COPY package.json .

RUN npm install

COPY . .

CMD ["npm","run","start"]
```

Running `docker build .` will look for the default `Dockerfile`, which does not exist at this time.
The build file must be explicitly defined using the `-f` flag:

```bash
  $ docker build -t sfdeloach/react-dev -f Dockerfile.dev .
```

Options added to the run command allow bookmarks and mappings to a volume. This will allow the
react development server the ability to detect changes made locally. Notice that both bookmarks
and mappings use the same `-v` flag. The only difference is the colon, which is a similar syntax
used earlier to map a container's port to the local machine's port:

```bash
  $ docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image id>
  #                          ^ bookmark           ^ mapping
```

This example is purposefully designed to demonstrate the use of volume bookmarks and volume maps.
In this example, we deleted the `node_modules` directory locally, which contained scripts needed to
start our development environment. Mapping the contents of our local working directory will not
provide it since it no longer exists. However, recall that the command `npm install` was run on
our container during the build. This installed a copy of `node_modules` in the container. The
bookmark tells the container to look inside its own file system for any references to the
`node_modules` directory.

As an aside, a simpler development container could be created. Only the `package.json` file would
be needed to run the initial npm script and only a mapping to the working directory is needed if
`node_modules` was not removed:

```Dockerfile
FROM node:alpine
WORKDIR '/app'
COPY package.json .
CMD ["npm","run","start"]
```

Build the image as shown above, then run with only the mapping:

```bash
  $ docker run -p 3000:3000 -v $(pwd):/app <image id>
```

The container would be able find `node_modules` on the local machine using this approach. Returning
to the contrived example that uses a bookmark for the `node_modules` directory, the run command is
rather lengthy. Docker Compose to the rescue!

```bash
  $ touch docker-compose.yml
```

The contents of `docker-compose.yml`:

```yml
version: "3"
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
# The context allows a reference to a different directory if the current directory is not the
# working directory.
```

To run tests, override the run command as demonstrated before:

```bash
  $ docker run -it <image id> npm run test
```

Running the command as demonstrated above causes a small problem. A new container is created with
its own filesystem, therefore, it is unable to detect any live changes to the source. There are
two solutions, each with advantages and disadvantages. The first solution uses the `exec` command
on the running running container:

```bash
  $ docker exec -it <container id> npm run test
```

The drawback on this approach requires a second step and keeping the container ID in mind. The
second solution is to setup an additional service in `docker-compose.yml`:

```Dockerfile
...
  (append this to the bottom of the existing file)
...

  tests:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - /app/node_modules
      - .:/app
    command: ["npm","run","test"]
```

The test results update as expected and they are conveniently started in its own container, however,
the terminal is not attached to the standard input, which does not allow for an interactive
experience. Consider which option may be best for your current testing objectives.

To this point in the exercise, we have setup a development and testing container. Now it is time to
move to production. This will be accomplished in a multi-step build process. In this case it will
occur in one `Dockerfile` that specifies two phases: **BUILD** and **RUN**

The _build phase_ will use `node:alpine` as a base image and install all dependencies in order to
build the react app.

The _run phase_ will use `nginx` as a base image, copy over the results of the _build phase_ and
start the Nginx server.

The multi phase `Dockerfile`:

```Dockerfile
FROM node:alpine as builder
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx
COPY --from=builder /app/build /usr/share/nginx/html
```

Note the following:

- it is not necessary to install all the dev dependencies in our production container
- in fact, node is not needed at all in production, we are only serving static content
- build stages can be named to increase readability: `FROM node:alpine as builder`
- no `RUN` command is necessary for nginx, the server is enabled by default

We are now ready to build our production image and run it:

```bash
  $ docker build .
  $ docker run -p 8080:80 <image id>
```

## CI/CD w/ AWS
