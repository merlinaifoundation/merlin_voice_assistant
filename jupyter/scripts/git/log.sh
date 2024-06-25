rm -rf LOG
echo "" >> LOG
#git log --pretty=format:"%s / %an / %ar" --graph --since=1days
#git log --pretty=format:"%s / %an" --since=1days >> LOG
git log --pretty=format:"%s / %an " --since=4hours >> LOG
cat LOG
cp LOG ../../RELEASE.txt
#git log --pretty=format:"%s / %an / %ar" --graph --since=1days
