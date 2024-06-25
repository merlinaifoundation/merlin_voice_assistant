#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'

###############################################

docker build -f tensor -t $CONTRIBUTOR/omc-tensor:latest .
docker push $CONTRIBUTOR/omc-tensor:latest



###############################################
###############################################

