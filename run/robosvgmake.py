import cairosvg
import os
import csv

datauri = '''data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xh
BQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAB
1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJh
ZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRm
OlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRm
LXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0i
IgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3Rp
ZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjE8L3RpZmY6Q29t
cHJlc3Npb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3Jp
ZW50YXRpb24+CiAgICAgICAgIDx0aWZmOlBob3RvbWV0cmljSW50ZXJwcmV0YXRp
b24+MjwvdGlmZjpQaG90b21ldHJpY0ludGVycHJldGF0aW9uPgogICAgICA8L3Jk
ZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KAtiABQAA
DCRJREFUaAW1WWtslFUafqedaWd6p7QgFKTYC1aQIggWkGUhJhgugiRGY7RZN2s0
IfvPP7sxWX9sNjEuPwj4R/ml2QRDopaLm03ELBSI3NpCoQUEhN7olWmnnXamc/n2
ec63Mz3fN98UMOUkM/N95/o+570954xLRAx8ZrysWLFCFixYINFoVG7duqU+M74I
JnQ/iUldLpe88847smrVKolEInLkyBE5cODAk1jqyQAwDEMuX74subm5EgqF5Jdf
fnkiwnPSGdeAz+cTj8cjL7zwgixdulRp4Ndff5ULFy7I6Oioep9JNJmY7JOZnHDL
li1SWVkpDx48EK/XK93d3XLu3Dl5+eWXlT/cv39/JpcTF2abcSemD+zdu1defPFF
teMNDQ2yf/9+oWnNdHkiAChkWVmZLFu2TAFobm4Wv98/07Kr+ab1gcxMWpi1cBfj
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
AABJRU5ErkJggg==
'''.replace('\n', '')

template = '''<?xml version="1.0"?>
<svg width="{outerwidth}" height="205" viewBox="0 0 {outerwidth} 205" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect x="0" y="0" rx="10" ry="10" width="{outerwidth}" height="205" style="fill: #000000" />
    <rect x="10" y="0" rx="10" ry="10" width="{innerwidth}" height="205" style="fill: #555555" />
    <text x="25" y="35" font-family="Courier, monospace" font-size="27" fill="#ffffff">Darby Robocode Battle #{battlenum}</text>
    {listings}
    <image x="{imagex}" y="79" width="48" height="48" xlink:href="{datauri}" />
</svg>
'''

listing = '''
    <text x="25" y="{y}" font-family="Courier, monospace" font-size="15" fill="#aaaaaa">{position}</text>
    <text x="35" y="{yplus15}" font-family="Courier, monospace" font-size="20" fill="#ffffff">{info}</text>
'''

# limit this at the max amount of robots to show
robotLinesStartWith = ['1st:', '2nd:', '3rd:', '4th:', '5th:']

def createListing(number, info):
    position = str(number) + ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][number % 10] + ':'
    y = 10 + (50 * number)
    return listing.format(y=y, yplus15=y+15, position=position, info=info)

def createWithLeaderboard(leaderboardPath):

    innerwidth = 440
    listings = ''
    
    with open(leaderboardPath, 'rb') as csvfile:
        leaderboardLines = csv.reader(csvfile, delimiter='\t')
    
        for line in leaderboardLines:
            print line
            if len(line) > 3:
                for i, prefix in robotLinesStartWith:
                    if line[0].startswith(prefix):
                        position = i + 1
                        info = line[0].split(' ')[1] + " - " + line[1].split(' ')[0]
                        innerwidth = max(innerwidth, 63 + int(len(info) * 11.7))
                        listings += createListing(position, info)

    outerwidth = innerwidth + 68
    imagex = outerwidth - 48 - 5

    out = template.format(datauri=datauri,
                          innerwidth=innerwidth,
                          outerwidth=outerwidth,
                          listings=listings,
                          imagex=imagex,
                          battlenum=os.environ['CIRCLE_BUILD_NUM'])
    return out

def writeFilesForSVG(svgstring, battle):
        f = open(os.path.expanduser('~/battles/results/' + battle + 'graphic.svg'), 'w')
        f.write(svgstring)
        f.close()
        
        fout = open(os.path.expanduser('~/battles/results/' + battle + 'graphic.png'), 'wb')
        cairosvg.svg2png(bytestring=svgstring.encode('utf-8'),write_to=fout)

        fout.close()

def create(battle):
    svg = createWithLeaderboard(os.path.expanduser('~/battles/results/' + battle + '.txt'))
    writeFilesForSVG(svg, battle)
