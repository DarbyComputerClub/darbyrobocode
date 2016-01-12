#!/bin/sh

git checkout gh-pages
git pull
mkdir results
cp -r ~/battles/* .
git config user.email '@' && git config user.name 'CircleCI'
git add .
git commit -m "Update published battles $1"
git push
git checkout master
