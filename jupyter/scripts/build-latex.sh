#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'


#does not work, wolframscript missing and is private
#docker build -f mathematica -t $CONTRIBUTOR/omc-mathematica:latest .
#docker push $CONTRIBUTOR/omc-mathematica:latest


###############################################

docker build -f latex -t $CONTRIBUTOR/merlin-dotnet-matlab-latex:latest --build-arg BUNDLE=dotnet-matlab .
docker push $CONTRIBUTOR/merlin-dotnet-matlab-latex:latest

docker build -f latex -t $CONTRIBUTOR/merlin-node-matlab-latex:latest --build-arg BUNDLE=node-matlab .
docker push $CONTRIBUTOR/merlin-node-matlab:latest

docker build -f latex -t $CONTRIBUTOR/merlin-node-dotnet-matlab-latex:latest --build-arg BUNDLE=node-dotnet-matlab .
docker push $CONTRIBUTOR/merlin-node-dotnet-matlab-latex:latest


