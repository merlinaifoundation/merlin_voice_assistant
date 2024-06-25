REG=$5
if [ ! $5 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "#################### $REG TITLE COMMIT ####################################"
echo ""
echo ""
PROTECTED_BRANCH="main"
BRANCH=$1
if [ ! $1 ]; then
  echo "Warning: No branch found... Using own's"
  BRANCH=$PROTECTED_BRANCH
fi
TIME_STAMP=$2
if [ ! $2 ]; then
  echo "Warning: No timestamp found... Using own's"
  TIME_STAMP=$(date +%s)
fi
TAG=$3
if [ ! $3 ]; then
  echo "Warning: No tag found... Using own's"
  TAG="preAlpha"
fi
#
VER=$4
if [ ! $4 ]; then
  VER=$(cat ../../VERSION | tr -d '\n')
  if [ ! $VER ]; then
    echo "Warning: No VER found... Using own's"
    VER="1.0.0"
  fi
fi
###########################################################################
#
SUFIX_ADD=${TIME_STAMP:6:4}
BUILD=${TIME_STAMP:0:4}
CODE_COLOR=${TIME_STAMP:4:2}

#VER=$(cat ../../VERSION | tr -d '\n')
CNAME=$(cat ../../CNFILE | tr -d '\n')
COLOR=$(cat ../../CDAY | tr -d '\n')

rm -rf CNAME.temp
echo "$CNAME" >> CNAME.temp
CNAME=$(cat CNAME.temp | tr a-z A-Z)
rm -rf CNAME.temp

TITLE="$CNAME ○ $COLOR ◄ $VER ► $CODE_COLOR.$TAG § $SUFIX_ADD"

rm -rf TITLE.temp
echo "$TITLE" >> TITLE.temp

echo "build id: $BUILD"
echo "title of commit: $TITLE"
echo "branch to clone from: $BRANCH"
echo "tag deployment: $TAG"
echo "ver deployment: $VER"


