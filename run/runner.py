#!/usr/bin/env python

import os
import pprint
import pip
import subprocess
import robosvgmake
import tournament
from robocoderun import robocoderun

battles = ["tournament/withsample","tournament/t2","tournament/t3","melee/darby","melee/withsample","1v1/enz_v_jac","1v1/jac_v_wall","1v1/enz_v_wall"]


run = [battles[i::int(os.environ['CIRCLE_NODE_TOTAL'])] for i in range(int(os.environ['CIRCLE_NODE_TOTAL']))]


print("List of Battles:i\n")
print(run)

print("\nRunning:")

battleList = run[int(os.environ['CIRCLE_NODE_INDEX'])]
print(battleList)

for battle in battleList:
    os.makedirs(os.path.expanduser('~/battles/results/' + os.path.dirname(battle)))
    if os.path.isfile('battles/' + battle + '.battle'):
        code = robocoderun('battles/' + battle + '.battle',
	                   os.path.expanduser('~/battles/results/' + battle + '.txt'),
			   os.path.expanduser('~/battles/results/' + battle + '.br'))
        if code != 0:
            exit(code)
    elif os.path.isfile('battles/' + battle + '.tournament'):
        print tournament.runTournamentCalled(battle)

    with open(os.path.expanduser('~/battles/results/' + battle + '-col.txt'), 'w') as w:
        w.write('Darby Robocode Battle\n')
        w.write(battle + ' #' + os.environ['CIRCLE_BUILD_NUM'] + '\n')
	with open(os.path.expanduser('~/battles/results/' + battle + '.txt'), 'r') as r:
	    w.write(r.read())
        w.write('\ncommit ' + os.environ['CIRCLE_SHA1'] + '\n')
    
    robosvgmake.create(battle)

# update the website
if os.environ['CIRCLE_BRANCH'] == 'master' and os.environ['CIRCLE_PROJECT_USERNAME'] == 'DarbyComputerClub' and not os.environ['CIRCLE_NODE_INDEX'] == '0':
        subprocess.call(['scp', '-r', os.path.expanduser('~/battles/'), 'ubuntu@node0:~/'])
