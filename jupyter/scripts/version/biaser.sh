#!/bin/bash

REG=$2
if [ ! $2 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "####################### $REG VERSION BIASER #############################"
echo ""
echo ""

DELTA=$1
if [ ! $1 ]; then
  #echo "Warning: No REG found... Using own's REG"
  DELTA=1
fi
#
OLD_BIAS=$(cat BIAS | tr -d '\n')
cat OLD_BIAS
#ALPHA_CODE=$1
rm -rf BIAS
BIAS=$(($OLD_BIAS - $DELTA))
echo "$BIAS" >> BIAS
cat BIAS
echo ""
echo ""
