#!/bin/sh

mkdir ~/results/
mv darbyrecord.br results-columns.txt ~/results/
git checkout gh-pages
git pull
cp ~/results/results-columns.txt ~/results/darbyrecord.br .
python imagemaker.py > battlegraphic.svg
git config user.email '@' && git config user.name 'CircleCI'
git add results-columns.txt darbyrecord.br battlegraphic.svg battlegraphic.png
git commit -m 'Update published battle'
git push
git checkout master
cp ~/results/results-columns.txt ~/results/darbyrecord.br . 
# so they are still available as artifacts
