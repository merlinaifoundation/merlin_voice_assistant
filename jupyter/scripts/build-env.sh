#!/bin/sh
REG=$2
if [ ! $2 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "#################### $REG BUILD ENV ####################################"
echo ""
echo ""

RNCDIR="./node_modules/react-native-config/ios"

if [ ! $ENV_PATH ]; then
  echo "Warning: No env_path found... Copied from argument $1!"
  ENV_PATH=$1
  if [ ${ENV_PATH:0:3} == "ENV" ];
    then
    ENV_PATH=${ENV_PATH:9}
    echo "Deleted ENV_PATH=prefix"
    else
    echo "No ENV_PATH prefix"
  fi
fi
echo "$ENV_PATH"

if [ ! $ENV_PATH ]; then
  echo "Warning: No $ENV_PATH file found... Copied .env.public to $ENV_PATH!"
  cp .env.development $ENV_PATH
fi

echo "Building environment config"
echo "Using $ENV_PATH"

if [ ! -z "$SYMROOT" ]; then
  # Ensure directories exist before copying files
  mkdir -p $SYMROOT
  mkdir -p $BUILD_DIR
  # Build dotenv
  cd $RNCDIR
  ./ReactNativeConfig/BuildDotenvConfig.ruby
  cd -
  # Copy generated dotenv files to node_modules directory
  cp "$BUILD_DIR/GeneratedInfoPlistDotEnv.h" "$RNCDIR/ReactNativeConfig/GeneratedInfoPlistDotEnv.h"
  cp "$SYMROOT/GeneratedDotEnv.m" "$RNCDIR/ReactNativeConfig/GeneratedDotEnv.m"
fi

# Generate dynamic environment for development
JSON="export default {$(cat $ENV_PATH | egrep "^[A-Za-z]+" | sed 's/\"/\\\"/g' | sed -n 's|\(.*\)=\(.*\)$|\1:'\'\\2\'',|p' | sed 's|\\\"||g') generatedAt: '$(date '+%FT%T')', }"
echo "Generating ./src/config.env.js"
echo $JSON > ./src/config.env.js
cat ./src/config.env.js
echo ""
echo ""
echo "Config built successfully!"
cp $ENV_PATH .env
cat .env
# Build config
echo ""
echo ""
echo "#################### $REG BUILD ENV ####################################"
