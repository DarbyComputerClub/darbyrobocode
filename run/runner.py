#!/usr/bin/env python

from subprocess import call
import os
import pprint
import pip
import subprocess
import robosvgmake

battles = ["melee/darby","melee/withsample","1v1/enz_v_jac","1v1/jac_v_wall","1v1/enz_v_wall"]

def bashrun(command):
    subprocess.call(['bash', '-c', command])


run = [battles[i::int(os.environ['CIRCLE_NODE_TOTAL'])] for i in range(int(os.environ['CIRCLE_NODE_TOTAL']))]


print("List of Battles:i\n")
print(run)

print("\nRunning:")

battleList = run[int(os.environ['CIRCLE_NODE_INDEX'])]
print(battleList)

for battle in battleList:
    os.makedirs(os.path.expanduser('~/battles/results/' + battle))
    bashrun("java -Xmx512M -Dsun.io.useCanonCaches=false -cp libs/robocode.jar robocode.Robocode -battle battles/" + battle + ".battle -nodisplay -results ~/battles/results/" + battle + ".txt -nosound -record ~/battles/results/" + battle + ".br")
    bashrun("cat <(echo \"Darby Robocode Battle number $CIRCLE_BUILD_NUM (from commit $CIRCLE_SHA1)\") <(column -ts $'\t' ~/battles/results/" + battle + ".txt) > ~/battles/results/" + battle + "-col.txt")
    
    robosvgmake.create(battle)


# update the website
if os.environ['CIRCLE_BRANCH'] == 'master' and os.environ['CIRCLE_PROJECT_USERNAME'] == 'DarbyComputerClub':
        subprocess.call([os.path.expanduser('~/run/geninfo.sh'), repr(battleList)])
