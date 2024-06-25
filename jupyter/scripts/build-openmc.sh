#!/bin/bash

  #
  CONTRIBUTOR=fulviofarina
  CONTRIBUTOR_KEY=$1


docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY

: '
'

###############################################

docker build -f openmc -t $CONTRIBUTOR/openmc:latest --build-arg build_dagmc=on --build-arg build_libmesh=on --build-arg compile_cores=4 .
docker push $CONTRIBUTOR/openmc:latest

###############################################




