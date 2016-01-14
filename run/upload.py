#!/usr/bin/env python

import os

# update the website
if os.environ['CIRCLE_BRANCH'] == 'master' and os.environ['CIRCLE_PROJECT_USERNAME'] == 'DarbyComputerClub' and not os.environ['CIRCLE_NODE_INDEX']:
        subprocess.call([os.path.expanduser('~/run/geninfo.sh')])
