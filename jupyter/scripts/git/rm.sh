#Sep 9th, 2021
#
# Git script for local branches cleanup & remote+local branch listing (LINUX)
REG=$1
if [ ! $1 ]; then
  #echo "Warning: No REG found... Using own's REG"
  REG="aiMonkey"
fi
echo "#################### $REG GITHUB LOCAL BRANCHES CLEANUP ####################################"
echo ""
echo ""

cd ..
#switch to any branch
git checkout buildAlpha
#delete local branches / Cleanup!
#git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D
git branch | grep -v "main" | xargs git branch -D
#switch to main branch
git checkout main
#fetch
git fetch
#list local & remotes
git branch -a

