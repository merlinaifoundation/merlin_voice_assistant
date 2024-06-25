#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'






docker build -f node -t $CONTRIBUTOR/omc-node:latest --build-arg NODE_VERSION=$NODE_VERSION .
docker push $CONTRIBUTOR/omc-node:latest

###############################################

