#!/usr/bin/env python

import os
import pprint
import pip
import subprocess
import robosvgmake

battles = ["melee/officers", "melee/all", "melee/newbots","melee/withsample","1v1/enz_v_jac","1v1/jac_v_wall","1v1/enz_v_wall"]


run = [battles[i::int(os.environ['CIRCLE_NODE_TOTAL'])] for i in range(int(os.environ['CIRCLE_NODE_TOTAL']))]


print("List of Battles:i\n")
print(run)

print("\nRunning:")

battleList = run[int(os.environ['CIRCLE_NODE_INDEX'])]
print(battleList)

for battle in battleList:
    os.makedirs(os.path.expanduser('~/battles/results/' + battle))
    exitcode = subprocess.call(['java', '-Xmx512M', '-Dsun.io.useCanonCaches=false', '-cp', 'libs/robocode.jar',
                                'robocode.Robocode',
	                        '-battle', 'battles/' + battle + '.battle',
	                        '-nodisplay',
	                        '-results', os.path.expanduser('~/battles/results/' + battle + '.txt'),
	                        '-nosound',
	                        '-record', os.path.expanduser('~/battles/results/' + battle + ".br")])
    if exitcode != 0:
        exit(exitcode)

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
