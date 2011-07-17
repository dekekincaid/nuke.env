# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# 
# Example builds a pan & tile rig from a single read node
#

import nuke

def panAndTile():

  #### error out if selected node is not a read ####
  read = nuke.selectedNode()
  if read.Class() != 'Read':
    nuke.message( "The selected node is not a read node" )
    return  
  curPos = (read['xpos'].value(), read['ypos'].value())
  
  #### Create knobs ####
  tabKnob = nuke.Tab_Knob('Panorama')
  focal = nuke.Double_Knob ( 'focal')
  haperture = nuke.Double_Knob ( 'haperture' )
  size = nuke.Double_Knob( 'size' )
  rotate = nuke.Double_Knob ( 'rotate' )
  tilt = nuke.Double_Knob( 'tilt' )
  turn = nuke.Enumeration_Knob( 'turn' , 'orientation', ('landscape', 'portrait'))
  
  ### set up sensible default values
  focal.setValue( 20 )
  focal.setRange(0, 100 )
  haperture.setValue( 36 )
  haperture.setRange( 0, 100 )
  size.setValue( 1 )
  size.setRange( 0,10000 )
  rotate.setValue( int( 360 / ( read['last'].value() - read['first'].value() + 1 ) ) )
  rotate.setRange( 0 , 360 )
  tilt.setValue( 30 )
  tilt.setRange( 0, 360 )
  turn.setValue( 1 )
  
  ####  create and add to scene node
  scene = nuke.nodes.Scene()
  
  for k in [tabKnob, focal, haperture, size, rotate, tilt, turn]:
    scene.addKnob( k )
    
  sceneExpr = 'parent.' + scene.name() + '.'
  
  ### loop through input images
  for i in range( read['first'].value(), read['last'].value() + 1 ):
    
    ### create frame hold
    frameHold = nuke.createNode( "FrameHold", inpanel = False )
    frameHold['postage_stamp'].setValue( True )
    frameHold['first_frame'].setValue( i )
    frameHold.setXYpos( int(curPos[0]+i*100 ), int(curPos[1]+100) )

    ### create card and set expressions
    card = nuke.createNode( "Card", inpanel = False ) 
    card['z'].setExpression( sceneExpr + 'size', 0 )
    card['lens_in_focal'].setExpression( sceneExpr + 'focal', 0 )
    card['lens_in_haperture'].setExpression( sceneExpr + 'haperture', 0 )
    
    card['rotate'].setExpression( sceneExpr + 'tilt', 0 )
    card['rotate'].setExpression( sceneExpr + 'rotate  * -' + str(i-1), 1 )
    card['rotate'].setExpression( sceneExpr + 'turn * 90' , 2 )
    card.setXYpos( int(curPos[0]+i*100), int(curPos[1]+200) )
    
    ### hook up nodes
    frameHold.setInput(0, read )
    card.setInput(0, frameHold )
    scene.setInput( i-1, card )
  scene.setXYpos( int(curPos[0]+(i*100/2)), int(curPos[1]+300) )
  
  
 
