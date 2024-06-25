#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'





docker build -f matlab -t $CONTRIBUTOR/omc-matlab:latest .
docker push $CONTRIBUTOR/omc-matlab:latest

#does not work, wolframscript missing and is private
#docker build -f mathematica -t $CONTRIBUTOR/omc-mathematica:latest .
#docker push $CONTRIBUTOR/omc-mathematica:latest

docker build -f latex -t $CONTRIBUTOR/omc-latex:latest .
docker push $CONTRIBUTOR/omc-latex:latest

###############################################




