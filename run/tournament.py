#!/usr/bin/env python
import pyjavaproperties
from robocoderun import robocoderun
import tempfile
import shutil
import random
import copy
import csv
import os

def loadFile(fpath):
    p = pyjavaproperties.Properties()
    with open(fpath, 'r') as f:
        p.load(f)
    return p

def saveFile(p, fpath):
    with open(fpath, 'w') as f:
        p.store(f)

def makeTempBattle(p):
    tempdir = tempfile.mkdtemp('', 'darbyrobocode_')
    saveFile(p, tempdir + '/a.battle')
    return tempdir

def separateProps(p):
    d = p.getPropertyDict()
    newp = pyjavaproperties.Properties()
    darbyopts = {}
    for key in d:
        if key.startswith('darby.'):
            darbykey = key.split('.', 1)[1]
            darbyopts[darbykey] = d[key]
        else:
            # Allow other options to go through to the battle file
            newp[key] = d[key]
    
    return newp, darbyopts

def getWinnerOfBattle(bot1, bot2, battletemplate):
    print battletemplate
    battle = battletemplate
    battle['robocode.battle.selectedRobots'] = ','.join([bot1, bot2])
    tempdir = makeTempBattle(battle)
    robocoderun(tempdir + '/a.battle', tempdir + '/results.txt', tempdir + '/results.br')
    with open(tempdir + '/results.txt', 'r') as r:
        lines = csv.reader(r, delimiter='\t')
        for line in lines:
            if len(line) > 0 and line[0].startswith('1st:'):
                return line[0][5:], tempdir

def getWinnerAndDiscard(bot1, bot2, battletemplate):
    winner, tempdir = getWinnerOfBattle(bot1, bot2, battletemplate)
    shutil.rmtree(tempdir)
    return winner


def splitList(l):
    split = []
    for i in range(int(len(l)/2)):
        split.append([l[2*i], l[2*i + 1]])
    if len(l) % 2 != 0:
        split.append(l[-1])
    return split

def retrieveWinners(botList, battletemplate):
    winnerList = []
    for pair in splitList(botList):
        if type(pair) == type([]):
            winnerList.append(getWinnerAndDiscard(pair[0], pair[1], battletemplate))
        else:
            winnerList.append(pair)
    return winnerList

def runTournament(botList, battletemplate):
    if len(botList) == 2:
        winner, tempdir = getWinnerOfBattle(botList[0], botList[1], battletemplate)
        loser = [l for l in botList if l != winner][0]
        return (winner, loser, tempdir,)
    else:
        winners = retrieveWinners(botList, battletemplate)
        return runTournament(winners, battletemplate)

def runTournamentCalled(name):
    p = loadFile('battles/' + name + '.tournament')
    battletemplate, darbyopts = separateProps(p)

    botsincluded = ['sample.Fire', 'sample.Crazy']
    for k in darbyopts:
        if k == 'tournament.selectedRobots':
            botsincluded = darbyopts[k].split(',')

    winner, loser, tempdir = runTournament(botsincluded, battletemplate)
    shutil.copyfile(tempdir + '/results.txt', os.path.expanduser('~/battles/results/' + name + '.txt'))
    shutil.copyfile(tempdir + '/results.br', os.path.expanduser('~/battles/results/' + name + '.br'))
