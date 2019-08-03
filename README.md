# docker
Notes on docker

## Manipulating Containers with the Docker Client
Verify installation:  
`docker run hello-world`

Info on installation:  
`docker version`

Create and run a container from image:  
`docker run <image name>`   

Default command override:  
`docker run <image name> command`

For example this prints "hi there" to terminal:  
`docker run busybox echo "hi there"`  

List of running containers:  
`docker ps`  

Container history:  
`docker ps --all`

The run command combines the create and start commands:  
`docker run <image name> = docker create <image name> + docker start <container id>`  

Creates image and provides a container id:  
`docker create <image name>`  

Starts the specified container, echos the id:  
`docker start <container id>`

The `-a` flag attaches to the running container:  
`docker start -a <container id>`  
A container can be restarted using the start command combined with the target container id  

Remove stopped containers:  
`docker system prune`  

Get logs from a container:  
`docker logs <container id>`

Stop a container (SIGTERM):  
`docker stop <container id>`  
If unsuccessful after 10 seconds, this command will revert to the kill command

Kill a containeri (SIGKILL):  
`docker kill <container id>`  
Does not allow the container to shutdown, `stop` command is preferred


