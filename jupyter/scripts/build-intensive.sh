#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'

###############################################

docker build -f tensor -t $CONTRIBUTOR/omc-tensor-node-dotnet:latest --build-arg BUNDLE=node-dotnet .
docker push $CONTRIBUTOR/omc-tensor-node-dotnet:latest

docker build -f latex -t $CONTRIBUTOR/omc-tensor-node-dotnet-latex:latest --build-arg BUNDLE=tensor-node-dotnet .
docker push $CONTRIBUTOR/omc-tensor-node-dotnet-latex:latest


docker build -f matlab -t $CONTRIBUTOR/omc-tensor-node-dotnet-matlab:latest --build-arg BUNDLE=tensor-node-dotnet .
docker push $CONTRIBUTOR/omc-tensor-node-dotnet-matlab:latest

#docker build -f mathematica -t $CONTRIBUTOR/omc-tensor-node-dotnet-matlab-mathematica:latest --build-arg BUNDLE=tensor-node-dotnet-matlab --build-arg .
#docker push $CONTRIBUTOR/omc-tensor-node-dotnet-matlab-mathematica:latest

###############################################

docker build -f latex -t $CONTRIBUTOR/omc-tensor-node-dotnet-matlab-latex:latest --build-arg BUNDLE=tensor-node-dotnet-matlab .
docker push $CONTRIBUTOR/omc-tensor-node-dotnet-matlab-latex:latest



###############################################
###############################################

