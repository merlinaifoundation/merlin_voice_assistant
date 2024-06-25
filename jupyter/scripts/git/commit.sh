REG=$4
if [ ! $4 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "#################### $REG GITHUB COMMIT ####################################"
echo ""
echo ""
PROTECTED_BRANCH="main"
BRANCH=$1
if [ ! $1 ]; then
  echo "Warning: No branch found... Using own's"
  BRANCH=$PROTECTED_BRANCH
fi
TARGET=$2
if [ ! $2 ]; then
  echo "Warning: No target found... Using own's"
  TARGET="development"
fi
TITLE=$3
if [ ! $3 ]; then

  TITLE=$(cat TITLE.temp)
  #if [ ! $TITLE ]; then
  #echo "Default: No TITLE found... Using own's"
  #TITLE="NoTitle"
  #else
  rm -rf TITLE.temp
  #fi
fi


echo "title of commit: $TITLE"
echo "branch to clone from: $BRANCH"
echo "target of commit: $TARGET"

###
echo "####################### $REG GITHUB CHECKOUT ##########################"
#
git checkout -b $TARGET origin/$BRANCH
#git checkout -b $TARGET origin/$TARGET
#git fetch
echo "####################### $REG GITHUB LOG ##########################"
#
sh log.sh
LOG=$(cat LOG)
rm -rf LOG
echo "####################### $REG GITHUB COMMIT ##########################"
#
git commit -a -m "$TITLE" -m "$LOG"
#
echo "####################### $REG GITHUB DELETE ##########################"
#
git push origin --delete $TARGET
#
echo "####################### $REG GITHUB PUSH ##########################"
#
git push --set-upstream origin $TARGET --tags

#notify Slack
cd ../deploy/ && bash postMsgSlack.sh "Branch commit :point_right: $TITLE :tanabata_tree: https://github.com/HarvestInc/lsd_v2/tree/$TARGET"
#
echo "####################### $REG GITHUB END ##########################"
#
#git checkout -b $ENV origin/$TARGET
#git commit -a -m "$CNAME.$CDAY: "$ID
#echo "#######################################################################"
#git push origin --delete $ENV
#git push --set-upstream origin $ENV

#git checkout $ENV # Switch to branch 'main'
#git merge $TARGET # merge to main
#git push --set-upstream origin $ENV
