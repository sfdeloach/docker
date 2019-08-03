 docker
Notes on docker

## Manipulating Containers with the Docker Client
`docker run hello-world` verify installation  
`docker version` info on installation  
`docker run <image name>` create and run a container from image  
`docker run <image name> command` default command override  
`docker run busybox echo "hi there"` prints "hi there" to terminal  
`docker ps` current list of running containers  
`docker ps --all` running container history  

The run command combines the create and start commands:
`docker run <image name> = docker create <image name> + docker start <container id>`  
`docker create <image name>` creates image and provides container id
`docker start <container id>` starts the specified container, echos the id
`docker start -a <container id>` the `-a` flag attaches to the running container
