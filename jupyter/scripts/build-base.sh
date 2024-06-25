#!/bin/bash
  NODE_VERSION=v22.3.19
  DOTNET_VERSION="8.0.203"
  #
  CONTRIBUTOR=fulviofarina
  CONTRIBUTOR_KEY=Fantasy23**
  #
  BUNDLE=node-dotnet
  INPUT_PATH=input
  HOST_PORT=4083
  CONTAINER_PORT=8888
  DATABASE_URL=postgresql://ffarina:Simionomatasimio1@3.75.169.55:5436/jupyterDB

  #NUSER: root/
  APP_PATH=WORKSPACE
  APP_TOKEN=omc123

  GROUP=harvestinc
  SERVICE_NAME=jupy3

docker logout

docker login -u $CONTRIBUTOR -p $CONTRIBUTOR_KEY


docker build -f base -t $CONTRIBUTOR/merlin-base:latest .
docker push $CONTRIBUTOR/merlin-base:latest

docker build -f extended -t $CONTRIBUTOR/merlin-extended:latest .
docker push $CONTRIBUTOR/merlin-extended:latest

docker build -f sql -t $CONTRIBUTOR/merlin-sql:latest .
docker push $CONTRIBUTOR/merlin-sql:latest

docker build -f lang -t $CONTRIBUTOR/merlin-lang:latest .
docker push $CONTRIBUTOR/merlin-lang:latest

###############################################


