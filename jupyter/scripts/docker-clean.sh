#!/bin/bash

#echo "List the service: $SERVICE_NAME"
#docker service ps $SERVICE_NAME
echo "PRUNE"
docker system prune -a -f
echo "PRUNE VOL"
docker volume prune -f
echo "LIST RESOURCES"
docker system df
