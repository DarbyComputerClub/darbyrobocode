#!/bin/sh

git checkout gh-pages
git pull
mkdir results
cp ~/results/* ./results/
python imagemaker.py > battlegraphic.svg
git config user.email '@' && git config user.name 'CircleCI'
git add .
git commit -m 'Update published battle'
git push
git checkout master
