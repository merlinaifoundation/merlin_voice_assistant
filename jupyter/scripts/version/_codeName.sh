#!/bin/bash
REG=$4
if [ ! $4 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi

echo "####################### $REG CODENAME EXTRACT #############################"
echo ""
echo ""
#
##
echo "BDAY: "
BUILD_DAY=$1
if [ ! $1 ]; then
  #echo "Warning: No REG found... Using own's REG"
  BUILD_DAY=0
fi
echo "$BUILD_DAY"

echo "CODENAME FILE NR: "
FILE_NR=$2
if [ ! $2 ]; then
  #echo "Warning: No REG found... Using own's REG"
  FILE_NR=1
fi
echo "$FILE_NR"

echo "CDAY: "
COLOR_DAY=$3
if [ ! $3 ]; then
  #echo "Warning: No REG found... Using own's REG"
  COLOR_DAY=0
fi
echo "$COLOR_DAY"

##
##
cat CODENAMES$FILE_NR
CNAME="monkey"
#
while IFS= read -r line; do
    NUMBER=${line:0:1}
    #this needs a space between argument and brakets
    if [ $NUMBER == $BUILD_DAY ];
    then
        CNAME=${line:2:20}
    fi
done < CODENAMES1
#


COLOR='yellow'
while IFS= read -r line; do
    NUMBER=${line:0:1}
    #this needs a space between argument and brakets
    if [ $NUMBER == $COLOR_DAY ];
    then
        COLOR=${line:2:20}
    fi
done < CODENAMES2
#


rm -rf CNFILE
rm -rf CDAY
echo $CNAME >> CNFILE
echo $COLOR >> CDAY
##
echo "CNFILE: "
cat CNFILE
##
echo "COLOR: "
cat CDAY

cp CNFILE ../../CNFILE
cp CDAY ../../CDAY

echo ""
echo ""
