#!/bin/sh

git checkout gh-pages
git pull
mkdir results
cp -r ~/battles/* ./results/



git config user.email '@' && git config user.name 'CircleCI'
git add .
git commit -m 'Update published battle'
git push
git checkout master
