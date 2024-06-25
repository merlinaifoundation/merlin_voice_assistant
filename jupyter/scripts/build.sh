#!/bin/bash


  #
  CONTRIBUTOR=fulviofarina
  CONTRIBUTOR_KEY=$1
  #
  BUNDLE=git
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

# Docker image build and push
echo "Building $SERVICE_NAME container image ..."

IMAGE=fulviofarina
TOKEN=$2
TEST_IMAGE=merlin
REPOSITORY=https://$TOKEN@github.com/eliastsoukatos/merlin_voice_assistant.git

echo "Building $IMAGE image"

###############################################3

echo "the CPORT is $CONTAINER_PORT "
echo "the APP_PATH is $APP_PATH "
echo "the APP_TOKEN is $APP_TOKEN "
echo "the INPUT_PATH is $INPUT_PATH "

echo "the BUNDLE is $BUNDLE "



docker build \
-f config \
-t $IMAGE/$TEST_IMAGE:latest \
--build-arg BUNDLE=$BUNDLE \
--build-arg CPORT=$CONTAINER_PORT \
--build-arg APP_PATH=$APP_PATH \
--build-arg APP_TOKEN=$APP_TOKEN \
--build-arg INPUT_PATH=$INPUT_PATH \
--build-arg REPOSITORY=$REPOSITORY \
--build-arg DATABASE_URL=$DATABASE_URL .
#
#docker tag $IMAGE:$CI_COMMIT_SHA $IMAGE:latest
#
#docker push --all-tags $IMAGE
