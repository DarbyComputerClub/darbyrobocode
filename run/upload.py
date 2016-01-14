# update the website
if os.environ['CIRCLE_BRANCH'] == 'master' and os.environ['CIRCLE_PROJECT_USERNAME'] == 'DarbyComputerClub':
        subprocess.call([os.path.expanduser('~/run/geninfo.sh')])
