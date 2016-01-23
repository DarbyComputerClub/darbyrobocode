#!/usr/bin/env python

import os
import subprocess

# update the website
if os.environ['CIRCLE_BRANCH'] == 'separate-results' and os.environ['CIRCLE_PROJECT_USERNAME'] == 'DarbyComputerClub' and os.environ['CIRCLE_NODE_INDEX'] == '0':
        subprocess.call([os.path.expanduser('~/run/geninfo.sh')])
