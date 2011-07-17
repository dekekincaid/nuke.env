
'''
[ Ym_alignNodes ver 1.5 ]     update. 03 Mar 2011 

-- Nuke align nodes tool --

This script helps to align messed up nodes.

1. align along X axis or Y axis.
2. align equal interval between each node. 

- Use -
Select nodes which you want to align and run.

- Notice -
This script is developing. 
Request of improvement :  feel free to contact me!

------------ Copyright (c) 2011 Yousuke Matsuno -------------
yousuke.matsuno@gmail.com / http://www.mat-vfx.com
-----------------------------------------------------------------------------
'''

import nuke

##---------- def ----------

def cmpX(cx1,cx2):

    ## get node center position
    cx1centX = cx1.xpos() + cx1.screenWidth() / 2
    cx2centX = cx2.xpos() + cx2.screenWidth() / 2

    if cx1centX < cx2centX:
        return -1
    else:
        return 0

def cmpY(cy1,cy2):

    ## get node center position
    cy1centY = cy1.ypos() + cy1.screenHeight() / 2
    cy2centY = cy2.ypos() + cy2.screenHeight() / 2

    if cy1centY < cy2centY:
        return -1
    else:
        return 0

##---------- align left X ----------

def alignLX():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []

    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpX)
    leftX =  scList[0].xpos() + scList[0].screenWidth() / 2

    for n in range(0,sn):     
        sizeGap = scList[n].screenWidth() / 2
        scList[n].setXpos(leftX - sizeGap)

##---------- align center X ----------

def alignCX():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpX)
    centX =  (scList[0].xpos() + scList[0].screenWidth() / 2) + ((scList[sn-1].xpos() + scList[sn-1].screenWidth() / 2) - (scList[0].xpos() + scList[0].screenWidth() / 2)) / 2
        
    for n in range(0,sn):     
        sizeGap = scList[n].screenWidth() / 2
        scList[n].setXpos(centX - sizeGap)

##---------- align right X ----------

def alignRX():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpX)
    rightX =  scList[sn-1].xpos() + scList[sn-1].screenWidth() / 2

    for n in range(0,sn):     
        sizeGap = scList[n].screenWidth() / 2
        scList[n].setXpos(rightX - sizeGap)

##---------- align top Y ----------

def alignTY():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpY)
    topY = scList[0].ypos() + scList[0].screenHeight() / 2

    for n in range(0,sn):     
        sizeGap = scList[n].screenHeight() / 2
        scList[n].setYpos(topY - sizeGap)

##---------- align center Y ----------

def alignCY():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpY)
    centY = (scList[0].ypos() + scList[0].screenHeight() / 2) + ((scList[sn-1].ypos() + scList[sn-1].screenHeight() / 2) - (scList[0].ypos() + scList[0].screenHeight() / 2)) / 2

    for n in range(0,sn):     
        sizeGap = scList[n].screenHeight() / 2
        scList[n].setYpos(centY - sizeGap)

##---------- align under Y ----------

def alignUY():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []

    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpY)
    underY = scList[sn-1].ypos() + scList[sn-1].screenHeight() / 2

    for n in range(0,sn):     
        sizeGap = scList[n].screenHeight() / 2
        scList[n].setYpos(underY - sizeGap)

##---------- align interval X ----------

def align_intX():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpX)
    intX = ((scList[sn-1].xpos() + scList[sn-1].screenWidth() / 2) - (scList[0].xpos() + scList[0].screenWidth() / 2)) / float (sn-1)

    for n in range(0,sn):
        xl = (scList[0].xpos() + scList[0].screenWidth() / 2) + (intX*n)
        sizeGap = scList[n].screenWidth() / 2
        scList[n].setXpos(xl - sizeGap)

##---------- align interval Y ----------

def align_intY():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []

    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpY)
    intY = ((scList[sn-1].ypos() + scList[sn-1].screenHeight() / 2) - (scList[0].ypos() + scList[0].screenHeight() / 2)) / float (sn-1)

    for n in range(0,sn):
        yl = (scList[0].ypos() + scList[0].screenHeight() / 2) + (intY*n)
        sizeGap = scList[n].screenHeight() / 2
        scList[n].setYpos(yl - sizeGap)

##---------- align interval XX ----------

def align_intXX():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpX)
    intX = ((scList[sn-1].xpos() + scList[sn-1].screenWidth() / 2) - (scList[0].xpos() + scList[0].screenWidth() / 2)) / float (sn-1)
    intY = ((scList[sn-1].ypos() + scList[sn-1].screenHeight() / 2) - (scList[0].ypos() + scList[0].screenHeight() / 2)) / float (sn-1)
    
    for n in range(0,sn):
        xl = (scList[0].xpos() + scList[0].screenWidth() / 2) + (intX*n)
        sizeGap = scList[n].screenWidth() / 2
        scList[n].setXpos(xl - sizeGap)
    
    for n in range(0,sn):
        yl = (scList[0].ypos() + scList[0].screenHeight() / 2) + (intY*n)
        sizeGap = scList[n].screenHeight() / 2
        scList[n].setYpos(yl - sizeGap)

##---------- align interval YY ----------

def align_intYY():
    s = nuke.selectedNodes()
    sn = len(s)
    if sn < 2: return

    scList = []
    
    for n in range(0,sn):
        newData = s[n]
        scList.append(newData)
    
    scList.sort(cmpY)
    intX = ((scList[sn-1].xpos() + scList[sn-1].screenWidth() / 2) - (scList[0].xpos() + scList[0].screenWidth() / 2)) / float (sn-1)
    intY = ((scList[sn-1].ypos() + scList[sn-1].screenHeight() / 2) - (scList[0].ypos() + scList[0].screenHeight() / 2)) / float (sn-1)

    for n in range(0,sn):
        yl = (scList[0].ypos() + scList[0].screenHeight() / 2) + (intY*n)
        sizeGap = scList[n].screenHeight() / 2
        scList[n].setYpos(yl - sizeGap)
    
    for n in range(0,sn):
        xl = (scList[0].xpos() + scList[0].screenWidth() / 2) + (intX*n)
        sizeGap = scList[n].screenWidth() / 2
        scList[n].setXpos(xl - sizeGap)