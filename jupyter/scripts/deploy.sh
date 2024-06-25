#!/bin/bash

echo "Setting ENV VARS Docker Registry: $DOCKER_REGISTRY/$GROUP ... ==> $SERVICE_NAME"
echo "Setting ENV SLUG and SHA: $CI_ENVIRONMENT_SLUG ... ==> $CI_COMMIT_SHA"

SERVICES=$(docker service ls --filter name=$SERVICE_NAME -q | wc -l)
IMAGE=$DOCKER_REGISTRY/$GROUP/$SERVICE_NAME/$CI_ENVIRONMENT_SLUG:$CI_COMMIT_SHA

docker logout
docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
docker pull $DOCKER_REGISTRY/$GROUP/$SERVICE_NAME/$CI_ENVIRONMENT_SLUG:$CI_COMMIT_SHA


if [[ "$SERVICES" -gt 0 ]]; then
  echo "Updating $SERVICE_NAME ... ==> $IMAGE"
  # Update service
echo "ECHO OF docker service update --with-registry-auth --image "$IMAGE" --replicas $REPLICAS --replicas-max-per-node $MAX_REPLICAS_PER_NODE --reserve-cpu $RESERVE_CPUS -d --publish-add $HOST_PORT:$CONTAINER_PORT \
--force $SERVICE_NAME"

#update service
docker service update --with-registry-auth --image "$IMAGE" --replicas $REPLICAS --replicas-max-per-node $MAX_REPLICAS_PER_NODE --reserve-cpu $RESERVE_CPUS -d --publish-add $HOST_PORT:$CONTAINER_PORT \
--force $SERVICE_NAME
#--env-add TARGET=$TARGET --env-add NODE_ENV=$NODE_ENV --env-add SESSION_SECRET=$SESSION_SECRET \
#--env-add DATABASE_URL=$DATABASE_URL \


else
  #docker network create --driver overlay $NETWORK || true
  echo "Creating $SERVICE_NAME ... ==> $IMAGE"
  echo "ECHO OF docker service create --with-registry-auth --name $SERVICE_NAME --replicas $REPLICAS --replicas-max-per-node $MAX_REPLICAS_PER_NODE --reserve-cpu $RESERVE_CPUS -d --network $NETWORK -p $HOST_PORT:$CONTAINER_PORT \
"$IMAGE""

  # Create service
docker service create --with-registry-auth --name $SERVICE_NAME --replicas $REPLICAS --replicas-max-per-node $MAX_REPLICAS_PER_NODE --reserve-cpu $RESERVE_CPUS -d --network $NETWORK -p $HOST_PORT:$CONTAINER_PORT \
"$IMAGE"
#--env TARGET=$TARGET --env NODE_ENV=$NODE_ENV --env SESSION_SECRET=$SESSION_SECRET \
#--env DATABASE_URL=$DATABASE_URL \
fi


#If the service NODE_LABEL var exist then constrain the deploy to a given node
if [[ "$NODE_LABEL" -gt 0 ]]; then

echo "Service constrained to Node: $NODE_LABEL"
#<<uncomment
  docker service update \
    --constraint-rm node.hostname==node$NODE_LABEL \
    --force \
    $SERVICE_NAME

  docker service update \
    --constraint-add node.hostname==node$NODE_LABEL \
    --force \
    $SERVICE_NAME
#uncomment

else
echo "Service not constrained to a specific node"
fi


#docker service rm haproxy
#docker service create --name haproxy --mount type=bind,source=/usr/local/app/haproxy/config,destination=/usr/local/etc/haproxy -p 80:80 -p 443:443 --network $NETWORK haproxy:latest
