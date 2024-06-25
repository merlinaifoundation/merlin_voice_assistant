#!/bin/bash
#copy certs!

CERTS_PATH=/docker-certs/docker-manager
#CERTS_PATH=/etc/docker

mkdir -p $CERTS_PATH
cd certs
cp ca.pem $CERTS_PATH/ca.pem
cp key.pem $CERTS_PATH/key.pem
cp cert.pem $CERTS_PATH/cert.pem

cat $CERTS_PATH/ca.pem
cat $CERTS_PATH/cert.pem
cat $CERTS_PATH/key.pem

CERTS_PATH_DOCKER=/etc/docker
mkdir -p $CERTS_PATH_DOCKER

cp ca.pem $CERTS_PATH_DOCKER/ca.pem
cp key.pem $CERTS_PATH_DOCKER/server-key.pem
cp cert.pem $CERTS_PATH_DOCKER/server-cert.pem
cd ..

#systemctl restart docker.service
#usermod -aG docker ubuntu
#docker swarm init
