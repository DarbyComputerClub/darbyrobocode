#!/usr/bin/env python
import pyjavaproperties
import tempfile
import shutil
import random
import copy

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

def getWinnerOfBattle(bot1, bot2):
    global battletemplate
    battle = copy.deepcopy(battletemplate)
    battle['robocode.battle.selectedRobots'] = ','.join([bot1, bot2])
    battle.list()
    return random.choice([bot1, bot2])

def splitList(l):
    split = []
    for i in range(int(len(l)/2)):
        split.append([l[2*i], l[2*i + 1]])
    if len(l) % 2 != 0:
        split.append(l[-1])
    return split

def retrieveWinners(botList):
    winnerList = []
    for pair in splitList(botList):
        if type(pair) == type([]):
            winnerList.append(getWinnerOfBattle(pair[0], pair[1]))
        else:
            winnerList.append(pair)
    return winnerList

def runTournament(botList):
    if len(botList) == 2:
        winner = getWinnerOfBattle(botList[0], botList[1])
        loser = [l for l in botList if l != winner][0]
        return (winner, loser,)
    else:
        winners = retrieveWinners(botList)
        return runTournament(winners)

def runTournamentCalled(name):
    global battletemplate
    p = loadFile('battles/' + name + '.tournament')
    battletemplate, darbyopts = separateProps(p)

    botsincluded = ['sample.Fire', 'sample.Crazy']
    for k in darbyopts:
        if k == 'tournament.selectedRobots':
            botsincluded = darbyopts[k].split(',')

    runTournament(botsincluded)
