#!/bin/bash

# ---
# Create certificates for connecting to docker swarm
# ---

echo "Creating certs for docker swarm ..."
CERTS_PATH=/docker-certs/docker-manager
#CERTS_PATH=/etc/docker

mkdir -p $CERTS_PATH
echo "$SWARM_MANAGER_TLS_CA" > $CERTS_PATH/ca.pem
echo "$SWARM_MANAGER_TLS_CERT" > $CERTS_PATH/cert.pem
echo "$SWARM_MANAGER_TLS_KEY" > $CERTS_PATH/key.pem

cat $CERTS_PATH/ca.pem
cat $CERTS_PATH/cert.pem
cat $CERTS_PATH/key.pem
