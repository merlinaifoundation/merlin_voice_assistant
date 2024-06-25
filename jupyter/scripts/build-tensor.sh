#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'

###############################################

docker build -f tensor -t $CONTRIBUTOR/merlin-tensor:latest .
docker push $CONTRIBUTOR/merlin-tensor:latest



###############################################
###############################################

