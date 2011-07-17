### version 0.3 on nuke 5.1v5###
### if you find bugs, or if you have any suggestions ###
### you can email me at papicrunch@gmail.com ###
### Papi ###

import nuke
import math

def Point2Axis():
    defaultFirstF = int(nuke.root().knob("first_frame").value())
    defaultLastF = int(nuke.root().knob("last_frame").value())
    defaultVersion = 1
    
    # panel 
    pPyScript = nuke.Panel("Parameter")
    pPyScript.addSingleLineInput("first Frame" , defaultFirstF)
    pPyScript.addSingleLineInput("last Frame" , defaultLastF)
    pPyScript.addSingleLineInput("version" , defaultVersion)
    pPyScript.addBooleanCheckBox("3d position:", True)
    pPyScript.addBooleanCheckBox("orient from surface:", True)
    pPyScript.addBooleanCheckBox("motion direction:", False)
    pResult = pPyScript.show()

    del defaultFirstF , defaultLastF , defaultVersion

    ##### check error #######

    if pResult != 1: #  for cancel panel
        del pResult , pPyScript
        return
    del pResult

    try: # frame integer
        firstFrameUser = int(pPyScript.value("first Frame"))
        lastFrameUser = int(pPyScript.value("last Frame"))
    except :
        nuke.message("frame must be an integer")
        return

    if firstFrameUser >= lastFrameUser : #for frame range error
        nuke.message("frame range error \n the last frame must be greater than the first frame")
        del pPyScript , firstFrameUser , lastFrameUser
        return

    versionUser = str(pPyScript.value("version"))
    curNode = nuke.thisNode() 
    curNodeName = str(curNode.name())
    curNameAxis = curNodeName +"\n" +str(firstFrameUser) + "," + str(lastFrameUser)+ " v" + versionUser
    curNameAxisCheck = nuke.toNode(curNameAxis)
    
    if curNameAxisCheck != None : #  for existing node
        nuke.message(curNameAxis +" already exist \n please increment your version")
        del pPyScript , firstFrameUser , lastFrameUser , curNameAxis , curNodeName
        del curNode , curNameAxisCheck , versionUser
        return

    del versionUser , curNameAxisCheck

    curNodeN = nuke.toNode(curNodeName +".input0") # access input0
    curNodeP = nuke.toNode(curNodeName +".input1") # access input1
    curNodeXY = curNode['point'] # access to self knob XY
    do3D = pPyScript.value("3d position:")
    doOrient = pPyScript.value("orient from surface:")
    doMotion = pPyScript.value("motion direction:")
    
    if curNodeP == None and do3D == True: #for no input node
        nuke.message("to find the 3d position\n \
        you need to connect a point position pass to input P")
        return

    if curNodeN == None and doOrient == True: #for no input node

        nuke.message("to find the orientation \n \
        you need to connect a normal pass to input N")
        return

    if do3D == False and doOrient == False and doMotion == False:
        nuke.message("probably you don't have any use of this node")
        return
        
    ##### end of check error #####
    
    # create AXIS
    curNode.end() #out of DAG
    curAxis = nuke.createNode("Axis")
    curAxis.setName(curNameAxis)
    curAxis['rot_order'].setValue('YZX')
    tColor = long(961231103)
    curAxis.knob('tile_color').setValue(tColor)
    del tColor
    
        
    knTranslate = curAxis['translate']
    knRotate = curAxis['rotate']
    knTranslate.setAnimated() #tx ty tz
    knRotate.setAnimated() #rx ry rz
    # allow access curves
    knTCurve = knTranslate.animations()
    knRCurve = knRotate.animations()
    incrFrame = firstFrameUser
    listPosX = []
    listPosY = []
    while incrFrame <= lastFrameUser: # sample frame by frame

        nuke.frame(incrFrame)       
        posX = curNodeXY.getValueAt(incrFrame,0)
        posY = curNodeXY.getValueAt(incrFrame,1)        
        if do3D == True:
            vTx = nuke.sample(curNodeP,1,posX,posY)
            vTy = nuke.sample(curNodeP,2,posX,posY)
            vTz = nuke.sample(curNodeP,3,posX,posY)
            knTCurve[0].setKey(incrFrame,vTx)
            knTCurve[1].setKey(incrFrame,vTy)
            knTCurve[2].setKey(incrFrame,vTz)
            del vTx , vTy , vTz

        if doOrient ==  True:
            vRx = -nuke.sample(curNodeN,2,posX,posY)*90+90
            vRz = -(nuke.sample(curNodeN,1,posX,posY))*90
            knRCurve[0].setKey(incrFrame,vRx)
            knRCurve[2].setKey(incrFrame,vRz)
            del vRx , vRz
        if doMotion == True:
            listPosX.append(posX) #list for Mdirection
            listPosY.append(posY) #list for Mdirection
        incrFrame = incrFrame+1
        del posX , posY
    
    
    if doMotion == True :# Mdirection create
        incrFrame = firstFrameUser
        while incrFrame < lastFrameUser:
            countList = incrFrame - firstFrameUser
            aXl , aYl = float(listPosX[countList]) , float(listPosY[countList])
            bXl , bYl = float(listPosX[countList+1]) , float(listPosY[countList+1])
            
            try:
                derivAB = (bYl - aYl)/(bXl-aXl)
            except:
                    derivAB = 0
            if derivAB < 0 and aXl < bXl:
                vRy = math.degrees(math.atan(derivAB))
                knRCurve[1].setKey(incrFrame,vRy)
            if derivAB > 0 and aXl < bXl:
                vRy = math.degrees(math.atan(derivAB))
                knRCurve[1].setKey(incrFrame,vRy)
            if derivAB < 0 and aXl > bXl:
                vRy = math.degrees(math.atan(derivAB)) - 180
                knRCurve[1].setKey(incrFrame,vRy)
            if derivAB > 0 and aXl > bXl:
                vRy = math.degrees(math.atan(derivAB)) - 180
                knRCurve[1].setKey(incrFrame,vRy)
            if aXl == bXl and aYl > bYl:
                vRy = -90
                knRCurve[1].setKey(incrFrame,vRy)
            if aXl == bXl and aYl < bYl:
                vRy = 90
                knRCurve[1].setKey(incrFrame,vRy)
            if aYl == bYl and aXl > bXl:
                vRy = -180
                knRCurve[1].setKey(incrFrame,vRy)
            if aYl == bYl and aXl < bXl:
                vRy = 0
                knRCurve[1].setKey(incrFrame,vRy)
                

            
            incrFrame = incrFrame+1
            del aXl , aYl , bXl , bYl
    del listPosX , listPosY
    del knTranslate , knRotate , knTCurve , knRCurve
    del curNode , curAxis , curNodeName , curNameAxis , incrFrame
    del curNodeN , curNodeP , curNodeXY

def PointProjection():
    # create group and inputs normal and pointPosition
    nName = "pointProjection"
    hpProj = """{pointProjection \n \
    help you to find where is an animated (or not)\n \
    2d point in your 3d space and orient object \n \
    according to the surface normal and direction of \n \
    the motion. \n \n \
    input N : Normal pass \n \
    input P : Point Position \n \
    P is needed to find the 3d position \n \
    N to find the orientation \n \
    the motion is determinate by the animated point \n \n \
    current limitation : \n \
    - P must be in world space \n \
    - N must be in range -1:1 \n \
    (same has nuke ScanlineRender) \n \
    - "the direction of motion" is experimental \n \
    if you use it, you certainly must tweak the rotate Y \n \
    \n papi}"""
    p3dProj = nuke.createNode("Group", "name "+ nName + " help " + hpProj , inpanel = True)
    tColor = long(961231103)
    p3dProj.knob('tile_color').setValue(tColor)
    del tColor    
    p3dProj.begin() # in DAG
    nuke.createNode("Input", "name N" , inpanel = False)
    nuke.createNode("NoOp", "name noOpN", inpanel = False)
    nuke.createNode("Input", "name P", inpanel = False)
    nuke.createNode("NoOp", "name noOpP", inpanel = False)
    p3dProj.end() # out DAG
          
    # interface
    p3dProj.addKnob(nuke.Tab_Knob("main"))
    posXY2d = nuke.XY_Knob("point")
    posXY2d.setTooltip("link or anim your point2d \n for the projection")
    p3dProj.addKnob(posXY2d)
    p3dProj.addKnob(nuke.Text_Knob(""))
    p3dProj.addKnob(nuke.PyScript_Knob("go","go !","papiTools.Point2Axis()"))
    p3dProj.addKnob(nuke.Text_Knob("pointProjection v0.3"))
    del p3dProj , posXY2d , nName
