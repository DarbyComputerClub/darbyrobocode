#!/usr/bin/env bash

if [ -d ~/gh-results/.git ]; then
    cd ~/gh-results
    git checkout -f gh-pages
    git pull
else
    git clone 'git@github.com:DarbyComputerClub/robocode-results.git' ~/gh-results
    git checkout -f gh-pages
fi
