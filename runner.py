#!/usr/bin/env python

from subprocess import call
import os
import pprint

call(["find robots/ -name '*.java' -print0 | xargs -0 javac -classpath "$CLASSPATH":./libs/robocode.jar:./robots -encoding UTF-8"])

def split(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

battles = ["melee/darby","1v1/enz_v_jac"]

run = split(battles, os.environ['CIRCLE_NODE_TOTAL'])

print("List of Battles:i\n")
pprint.pprint(list(run))
print("\nRunning:")
pprint.pprint(list(run[os.environ['CIRCLE_NODE_INDEX']]))

for battle in run[os.environ['CIRCLE_NODE_INDEX']]:
    call(["java -Xmx512M -Dsun.io.useCanonCaches=false -cp libs/robocode.jar robocode.Robocode -battle battles/" + battle + ".battle -nodisplay -results ~/battles/results-" + battle + ".txt -nosound -record ~/battles/record" + battle + ".br"])
    call(["cat <(echo \"Darby Robocode Battle number $CIRCLE_BUILD_NUM (from commit $CIRCLE_SHA1)\") <(column -ts $'\t' ~/battles/results-" + battle + ".txt) > ~/battles/results-" + battle + "-col.txt"])

