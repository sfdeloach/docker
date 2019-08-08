# docker
Notes on docker

## Dive into Docker!
**image**
> Containers are created from images. Think of a cookie cutter.

**container**
> An instance of an image. Think cookie.

## Manipulating Containers with the Docker Client

Verify installation:  
`docker run hello-world`

Info on installation:  
`docker version`

Create and run a new container from image:  
`docker run <image name>`   
> If the image is not already loaded then it will pull the image from the repo before it starts

Default command override:  
`docker run <image name> command`

For example this prints "hi there" to terminal:  
`docker run busybox echo "hi there"`  

List of running containers:  
`docker ps`  
> Alias for `docker container ls`. By default, only running containers in the local repo are listed.

List of all containers, running and stopped:  
`docker ps -a`  
> The `-a` flag is short for `--all`. See `man docker container-ls` for more info.

The run command combines the create and start commands:  
`docker run <image name> = docker create <image name> + docker start <container id>`  

Creates a new container from an image:  
`docker create <image name>`  

Starts the specified container, echos the id:  
`docker start <container id>`

The `-a` flag attaches to the running container:  
`docker start -a <container id>`  
> A container can be restarted using the start command combined with the target container id  

Remove stopped containers:  
`docker system prune`  

Get logs from a container:  
`docker logs <container id>`

Stop a container (SIGTERM):  
`docker stop <container id>`  
> If unsuccessful after 10 seconds, this command will revert to the kill command

Kill a container (SIGKILL):  
`docker kill <container id>`  
> Does not allow the container to shutdown, `stop` command is preferred

Multi-command containers:  
`docker exec -it <container id> <command>`  
> Run a command in a running container. The `-i` keeps STDIN open and will make the session
interactive. The `-t` flag will allocate a pseudo-TTY and make the session prettier.  

Getting a command prompt in a container:  
`docker exec -it <container id> bash`  
> Provides interactive bash shell on a running container.

Run a new container and start in a shell:  
`docker run -it <image name> sh`  

Run a new Ubuntu container and start in a bash shell:  
`docker run -it ubuntu bash`  
> Docker containers run in completed isolated filesystems.

View docker images on your local machine:  
`docker image ls`  

## Building Custom Images Through Docker Server

Custom images are built with a `Dockerfile`:  

```Dockerfile
# Use an existing docker image as a base
FROM alpine

# Download and install a dependency
RUN apk add --update redis

# Tell the image what to do when it starts as a container
CMD ["redis-server"]
```

Building the image (command executed from the same directory as `Dockerfile`):  
`docker build .`  
> Docker will cache dependencies for faster rebuilds

Build an image with repository info, name, and tag (version):  
`docker build -t sfdeloach/redis:latest .`  
> By convention, the tag is prefixed with your Docker ID

Another (nonsensical) example using Fedora and NodeJs:  

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

See the file `node-express-Dockerfile` for an example of how to build a nodeJS express server image
using a Dockerfile. Take notice of the following "how to's":

- specify a tag with a base image
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

See `docker-compose-example` for a small project. The containers are build by running the command
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

