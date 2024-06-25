#!/bin/bash

echo "Signing into docker registry ..."
echo "Registry $CI_REGISTRY and $CI_REGISTRY_USER registry user ..."
docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

# ---
# Deploy service
# ---
echo "Network Check $NETWORK ..."
NETWORK_NAME=$(docker network ls --filter name=$NETWORK -q | wc -l)
#
if [[ "$NETWORK_NAME" -gt 0 ]]; then
echo "The Network already exist"
else
echo "The Network does not exist... SWARM INIT"
docker swarm leave --force
docker system prune -a -f
docker swarm init
echo "Create Network $NETWORK"
docker network create --driver overlay $NETWORK || true
fi

