#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'






###############################################

docker build -f dotnet -t $CONTRIBUTOR/omc-node-dotnet:latest --build-arg BUNDLE=node --build-arg DOTNET_VERSION=$DOTNET_VERSION .
docker push $CONTRIBUTOR/omc-node-dotnet:latest

###############################################


