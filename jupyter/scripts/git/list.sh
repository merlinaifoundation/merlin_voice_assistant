
TARGET=$1
if [ ! $1 ]; then
  #echo "Warning: No timestamp found... Using own's branch"
  TARGET=$(date +%s)
  TARGET=${TARGET:0:4}
fi
cd ../..
rm -rf LIST.temp
git remote prune origin
#git fetch
git branch -r -l *$TARGET* >> LIST.temp
#git show-branch -r --list >> LIST.temp
cat LIST.temp
#cp LIST.temp ../../LIST.temp

