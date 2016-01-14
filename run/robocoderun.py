import subprocess

def robocoderun(battlefile, resultsfile, recordfile):
    code = subprocess.call(['java', '-Xmx512M', '-Dsun.io.useCanonCaches=false', '-cp', 'libs/robocode.jar',
                            'robocode.Robocode',
                            '-battle', battlefile,
                            '-nodisplay',
                            '-results', resultsfile,
                            '-nosound',
                            '-record', recordfile])
    return code
