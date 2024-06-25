#!/bin/bash

docker logout


CONTRIBUTOR=fulviofarina
CONTRIBUTOR_KEY=$1
NODE_VERSION=v22.3.19

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'






docker build -f node -t $CONTRIBUTOR/merlin-node:latest --build-arg NODE_VERSION=$NODE_VERSION .
docker push $CONTRIBUTOR/merlin-node:latest

###############################################

