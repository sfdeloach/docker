image ubuntu:24.04

apt update
apt upgrade -y
apt install -y golang-go ca-certificates curl git wget

working directory: /usr/src/app
*copy files into working directory*

go mod init example
go get github.com/a-h/templ
go install github.com/a-h/templ/cmd/templ@latest

export PATH=$HOME/go/bin:$PATH
