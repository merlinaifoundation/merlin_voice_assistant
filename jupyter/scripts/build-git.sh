#!/bin/bash

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'


docker build -f git -t $CONTRIBUTOR/omc-git:latest --build-arg GIT_VERSION=$GIT_VERSION .
docker push $CONTRIBUTOR/omc-git:latest


###############################################


