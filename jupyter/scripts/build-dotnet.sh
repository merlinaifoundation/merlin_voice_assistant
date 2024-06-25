#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'






docker build -f dotnet -t $CONTRIBUTOR/omc-dotnet:latest --build-arg DOTNET_VERSION=$DOTNET_VERSION .
docker push $CONTRIBUTOR/omc-dotnet:latest



