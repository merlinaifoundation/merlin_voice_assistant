REG=$3
if [ ! $3 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "#################### $REG GITHUB COMMIT ####################################"
echo ""
echo ""
#
TARGET=$2
BRANCH=$1
echo "#######################################################################"
git checkout -b $TARGET origin/$BRANCH
git push origin --delete $TARGET
echo "#######################################################################"
git push --set-upstream origin $TARGET
