#!/bin/bash

docker logout


CONTRIBUTOR=fulviofarina
CONTRIBUTOR_KEY=$1

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'






###############################################

docker build -f dotnet -t $CONTRIBUTOR/merlin-node-dotnet:latest --build-arg BUNDLE=node --build-arg DOTNET_VERSION=$DOTNET_VERSION .
docker push $CONTRIBUTOR/merlin-node-dotnet:latest

###############################################


