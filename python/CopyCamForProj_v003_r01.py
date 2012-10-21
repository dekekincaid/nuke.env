# Projection Camera Copy
# Nuke Python Module
#
# Copy to for Projection Camera with a slider and the ability to change dynamically the frame you are projecting on
#
#
#
# Created by Marco Leone on 8/02/2012
#  marco.leone87@gmail.com
#
# version 3.1 on 02/03/2012
# fexed bug Camera Tracker
#
#
#
# Copyright 2012 Marco Leone
#  http://www.marcoleone.net
#  All rights reserved
#
#
#
#
#
#
import nuke

def copyCamForProj():

        node=nuke.selectedNode()
        BOOL=["focal","haperture","vaperture","near","far","win_translate","win_scale","winroll","focal_point","fstop","xform_order","rot_order"]
        LIST_KNOB=[]
        print BOOL
        for k in node.knobs() :

            if node[k].isAnimated() :

                LIST_KNOB.append(k)
                if k in BOOL:
                    BOOL.pop(BOOL.index(k))

        print LIST_KNOB
        print BOOL



         #
        MIN_MAX=[]

        firstFrame= nuke.Root()['first_frame'].value()
        lastFrame=nuke.Root()['last_frame'].value()

        MIN_MAX.append(firstFrame)
        MIN_MAX.append(lastFrame)

        print MIN_MAX


        if (node.Class() == 'Camera2') or (node.Class() == 'Camera'):

                projCam=nuke.createNode('Camera2')
                projCam.setName('ProjCam')
                projCam['tile_color'].setValue(169550)
                a=nuke.WH_Knob('projFrame','Projection Frame')


                a.setRange(MIN_MAX[0],MIN_MAX[1])

                a.setTooltip('choose the frame you want to project')

                projCam.addKnob(a)
                ### thanks Sirak
                projCam['projFrame'].setValue(MIN_MAX[0])



                for i in projCam.knobs():

                        if i in LIST_KNOB:

                                projCam.knob(i).setExpression("%s.%s(projFrame)" % (node.name(), node.knob(i).name()))

                projCam['useMatrix'].setValue(1)
                projCam['matrix'].setExpression("%s.matrix(projFrame)" % node.name())

                VALUE=[]

                for i  in BOOL:
                    if i  in LIST_KNOB:
                        BOOL.pop(BOOL.index(i))
                        print'\n'
                        print BOOL
                for i in BOOL:
                    if i not in LIST_KNOB:
                        VALUE.append(node[i].value())
                        print VALUE


                        print '\n'
                        print BOOL
                        print VALUE
                a=BOOL[-1]

                print a

                b= int (BOOL.index(a)+1)

                print b
                print'\n'

                for i in range(0,b):
                        print BOOL[i]
                        print VALUE[i]
                        projCam[BOOL[i]].setValue(VALUE[i])

                projCam['label'].setValue('(frame [value projFrame])')
                button=nuke.PyScript_Knob('currFrame', 'Current Frame','node=nuke.thisNode()\nnode["projFrame"].setValue(nuke.frame())')
                projCam.addKnob(button)
        else :
                nuke.message("Oops, you didn't selected a Camera!")


# keyboard shortcut for this command
#menu = nuke.menu('Nuke')
#MyScripts=menu.addMenu('My Scripts')
#MyScripts.addCommand( 'Copy Camera for Projection', 'copyCamForProj()', "Shift+v")
