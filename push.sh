#!/bin/bash


function git_branch {
   branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
   if [ "${branch}" != "" ];then
       if [ "${branch}" = "(no branch)" ];then
           branch="(`git rev-parse --short HEAD`...)"
       fi
       echo $branch
   fi
}

git add .

git commit -m "`date`"

git push origin `git_branch`

git push open `git_branch`

git push lykan  `git_branch`
