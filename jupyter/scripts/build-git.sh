#!/bin/bash

CONTRIBUTOR=fulviofarina
CONTRIBUTOR_KEY=$1
GIT_VERSION="2.39.5"
#https://mirrors.edge.kernel.org/pub/software/scm/git/
docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'

docker build -f git -t $CONTRIBUTOR/merlin-git:latest --build-arg GIT_VERSION=$GIT_VERSION .
docker push $CONTRIBUTOR/merlin-git:latest


###############################################


