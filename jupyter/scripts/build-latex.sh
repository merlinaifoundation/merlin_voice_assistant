#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'


#does not work, wolframscript missing and is private
#docker build -f mathematica -t $CONTRIBUTOR/omc-mathematica:latest .
#docker push $CONTRIBUTOR/omc-mathematica:latest


###############################################

docker build -f latex -t $CONTRIBUTOR/omc-dotnet-matlab-latex:latest --build-arg BUNDLE=dotnet-matlab .
docker push $CONTRIBUTOR/omc-dotnet-matlab-latex:latest

docker build -f latex -t $CONTRIBUTOR/omc-node-matlab-latex:latest --build-arg BUNDLE=node-matlab .
docker push $CONTRIBUTOR/omc-node-matlab:latest

docker build -f latex -t $CONTRIBUTOR/omc-node-dotnet-matlab-latex:latest --build-arg BUNDLE=node-dotnet-matlab .
docker push $CONTRIBUTOR/omc-node-dotnet-matlab-latex:latest


