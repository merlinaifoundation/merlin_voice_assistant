#!/bin/bash

REG=$2
if [ ! $2 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "####################### $REG VERSION EXTRACT #############################"
echo ""
echo ""
#timestamp
TIME_STAMP=$1
if [ ! $1 ]; then
  echo "Warning: No timestamp found... Using own's timestamp"
  TIME_STAMP=$(date +%s)
fi
echo "TSTAMP: $TIME_STAMP"
##
##
BUILD_EPOCH=${TIME_STAMP:0:5}
echo "BUILD_EPOCH: "
#
rm -rf BUILD_NR
echo "$BUILD_EPOCH" >> BUILD_NR
cat BUILD_NR

BUILD_EPOCH_DAY=${TIME_STAMP:4:1}
echo "BDAY: "
rm -rf BDAY
echo "$BUILD_EPOCH_DAY" >> BDAY
cat BDAY
cp BDAY ../../BDAY
echo "Copied BDAY"

COLOR=${TIME_STAMP:5:1}
echo "COLOR: "
rm -rf CDAY
echo "$COLOR" >> CDAY
cat CDAY
cp CDAY ../../CDAY
echo "Copied COLOR"
#
echo "BIAS: "
BIAS=$(cat BIAS | tr -d '\n')
cat BIAS
#
echo "VNUM: "
VNUM=$(($BUILD_EPOCH - $BIAS))
rm -rf VNUM
echo "$VNUM" >> VNUM
cat VNUM
#
VNUM=$(cat VNUM | tr -d '\n')
MAJOR=${VNUM:0:1}
MINOR=${VNUM:1:1}
PATCH=${VNUM:2:2}
#
rm -rf VERSION
echo "$MAJOR.$MINOR.$PATCH" >> VERSION
#
#

echo "VERSION: "
cat VERSION
cp VERSION ../../VERSION
echo "Copied VERSION"
echo ""
echo ""
