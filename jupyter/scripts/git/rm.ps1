#Sep 9th, 2021
#
# Git script for local branches cleanup & remote+local branch listing (WINDOWS)

#switch to any branch
git checkout buildAlpha
#delete local branches / Cleanup!
git branch | %{ $_.Trim() } | ?{ $_ -ne 'main' } | %{ git branch -D $_ }
#switch to main branch
git checkout main
#fetch
git fetch
#list local & remotes
git branch -a
