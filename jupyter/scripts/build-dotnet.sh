#!/bin/bash

docker logout


CONTRIBUTOR=fulviofarina
CONTRIBUTOR_KEY=Fantasy23**
DOTNET_VERSION="8.0.203"

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'




docker build -f dotnet -t $CONTRIBUTOR/merlin-dotnet:latest --build-arg DOTNET_VERSION=$DOTNET_VERSION .
docker push $CONTRIBUTOR/merlin-dotnet:latest



