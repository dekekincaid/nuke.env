# mocha_import for Nuke
# by michael@yawpitchroll.com
# last modified 03/19/2008
# directions for installation at fxshare.com

"""
mocha_import for Nuke 5.X and Mocha 1.2.0:
Imports tracking data exported from Mocha as either Nuke ASCII (one .txt file per corner) or Shake .shk
"""

import nuke

def _getfilename():
    """
    Asks user for the filename to be imported.  Filters the import routine to just the acceptable file types.
    """
    filename = nuke.getFilename("Mocha Tracking Export (Nuke ASCII or Shake Format)", "*_Tracker?.txt;*.shk")
    return filename

def _asciishapename(filename):
    """
    Parses the shapename out of the export file name (ASCII pathway)
    """
    shapeName = "mocha." + filename[(max(filename.rfind('/'), filename.rfind('\\'))+1):-13]
    return shapeName

def _asciiparse(filename):
    """
    Parses the tracking data out of the export file(s) (ASCII pathway).  All files must remain as named by Mocha (ie, _TrackerN,txt with N = [1,2,3,4])
    """
    filename = filename
    mocha_filetest = ['_Tracker1.txt','_Tracker2.txt','_Tracker3.txt','_Tracker4.txt']
    truncName = filename[:-13]
    fileList = [truncName + filetest for filetest in mocha_filetest]
    start = int(nuke.animationStart())
    formattedList = []
    for file in fileList:
        procFile = open(file)
        alldata = [line.rstrip().split(' ') for line in procFile]
        trackStart = "{curve L x" + str(start)
        trackBodyX, trackBodyY = '',''
        for coord in alldata:
            trackBodyX += " " + coord[0]
            trackBodyY += " " + coord[1]
        trackBodyX += "}"
        trackBodyY += "}"
        trackTxt = trackStart + trackBodyX + " " + trackStart + trackBodyY
        formattedList.append(trackTxt)
    unpackedList = [formattedList[0], formattedList[1], formattedList[3], formattedList[2]]
    return unpackedList

def _ascii_import(filename):
    """
    Runs the import once the ASCII pathway has been chosen.
    """
    shapeName = _asciishapename(filename)
    imported = _asciiparse(filename)
    return (imported, shapeName)

def _shkscrub(filename):
    """
    Parses the .shk file and returns the parsed (but not formatted) list and the shapename as a tuple. (.shk pathway)
    """
    rawList = []
    parseList = []

    # cuts off the excess file that is part of the shake mocha export
    for line in open(filename):
        fileEndTest = ('= Stabilize(')
        lineStartTest = ('Linear(')
        lineEndTest = ('),\n')
        nameStartTest = ('CornerPin')
        nameEndTest = (' = CornerPin(')
        if fileEndTest in line:
            break
        elif nameEndTest in line:
            shapeName = line[:line.find(nameEndTest)]
            shapeName = shapeName.replace(nameStartTest,'')
            shapeName = "mocha." + shapeName
        elif lineStartTest in line:
            line=line.replace(lineStartTest,'')
            line=line.replace(lineEndTest,'')
            rawList.append(line)
        
    for axis in rawList:
        frameTest = ('@')
        cleanParse = []
        parse = axis.split(',')
        for datum in parse:
            if frameTest in datum:
                parsedatum = tuple(datum.split(frameTest))
                parsed = (int(parsedatum[1]),parsedatum[0])
                cleanParse.append(parsed)
        axis = cleanParse
        parseList.append(axis)
        
    return (parseList,shapeName)

def _shkreformat(scrubbedlist):
    """
    Formats the parsed .shk tracking data (.shk pathway)
    """
    formattedList = []
    unpackedList = []
    for axis in scrubbedlist:
        trackTxt = "{curve L "
        lastframe = None
        for framerec in axis:
            try:
                framerec[0] == (lastframe + 1)
            except:
                trackTxt += ' x' + str(framerec[0])
                trackTxt += ' '
                trackTxt += framerec[1]
            else:
                trackTxt += ' '
                trackTxt += framerec[1]
            try:
                lastframe += framerec[0]
            except:
                lastframe = framerec[0]

        trackTxt += '}'
        formattedList.append(trackTxt)
    unpackedList = [(formattedList[0] + ' ' + formattedList[1]),(formattedList[2] + ' ' +  formattedList[3]),(formattedList[4] + ' ' +  formattedList[5]),(formattedList[6] + ' ' +  formattedList[7]),]
    return unpackedList

def _shk_import(filename):
    """
    Runs the import once the .shk pathway has been chosen.
    """
    initialized = _shkscrub(filename)
    shapeName = initialized[1]
    imported = _shkreformat(initialized[0])
    return (imported, shapeName)
    
def mocha_import():
    """
    Asks the user for the filename to be imported, then decides the pathway and builds the appropriate Tracker node.
    """
    initial = _getfilename()
    imported = []

    if initial.endswith('.txt'):
        imported = _ascii_import(initial)
    elif initial.endswith('.shk'):
        imported = _shk_import(initial)
    else:
        print "That file is not a .txt or a .shk"
    
    track1 = str(imported[0][0])
    track2 = str(imported[0][1])
    track3 = str(imported[0][2])
    track4 = str(imported[0][3])
    shapeName = str(imported[1])

    tk = nuke.createNode("Tracker3")
    tk.knob("track1").fromScript(track1)
    tk.knob("track2").fromScript(track2)
    tk.knob("track3").fromScript(track3)
    tk.knob("track4").fromScript(track4)
    tk.knob("label").setValue(shapeName)
    tk.knob("enable1").setValue(True)
    tk.knob("enable2").setValue(True)
    tk.knob("enable3").setValue(True)
    tk.knob("enable4").setValue(True)
    tk.knob("use_for1").fromScript('all')
    tk.knob("use_for2").fromScript('all')
    tk.knob("use_for3").fromScript('all')
    tk.knob("use_for4").fromScript('all')

