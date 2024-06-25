#!/bin/bash

# ---
echo "Listing networks..."
docker network ls
echo "Listing service..."
docker service ls
echo "Listing container..."
docker container ls
echo "Docker System DF..."
docker system df
#
