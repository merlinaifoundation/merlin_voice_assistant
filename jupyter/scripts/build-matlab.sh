#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'


#does not work, wolframscript missing and is private
#docker build -f mathematica -t $CONTRIBUTOR/omc-mathematica:latest .
#docker push $CONTRIBUTOR/omc-mathematica:latest


###############################################

docker build -f matlab -t $CONTRIBUTOR/omc-dotnet-matlab:latest --build-arg BUNDLE=dotnet .
docker push $CONTRIBUTOR/omc-dotnet-matlab:latest

docker build -f matlab -t $CONTRIBUTOR/omc-node-matlab:latest --build-arg BUNDLE=node .
docker push $CONTRIBUTOR/omc-node-matlab:latest

docker build -f matlab -t $CONTRIBUTOR/omc-node-dotnet-matlab:latest --build-arg BUNDLE=node-dotnet .
docker push $CONTRIBUTOR/omc-node-dotnet-matlab:latest





