#!/bin/bash

CONTRIBUTOR=fulviofarina
CONTRIBUTOR_KEY=Fantasy23**
GIT_VERSION="2.45.1"

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'

docker build -f git -t $CONTRIBUTOR/merlin-git:latest --build-arg GIT_VERSION=$GIT_VERSION .
docker push $CONTRIBUTOR/merlin-git:latest


###############################################


