#Menu.py
#this sets default formats,adds custom menu gizmos, shortcuts, python/tcl scripts
#
#dekekincaid@gmail.com
#Tested with Nuke 5.2, 6.0, 6.1, 6.2, 6.3
#won't run under 5.1.x as is

#defines default format resolutions
nuke.addFormat ("720 540 0 0 720 540 1.0 NTSC_square")
nuke.addFormat ("960 540 0 0 960 540 1.0 540p")
nuke.addFormat ("1280 720 0 0 1280 720 1.0 720p")
#nuke.addFormat ("1920 1440 0 0 1920 1440 1.0 1920_4x3")
#nuke.addFormat ("960 720 0 0 960 720 1.0 1920_4x3_half")
nuke.addFormat ("3840 2160 0 0 3840 2160 1.0 HD_double")
nuke.addFormat ("4096 4096 0 0 4096 4096 1.0 4k_square")
#nuke.addFormat ("2048 1108 0 0 2048 1108 1.0 2k_185_crop")
#nuke.addFormat ("2048 1157 0 0 2048 1157 1.0 2k_3perf_crop")
#nuke.addFormat ("2048 872 0 0 2048 872 1.0 2k_235_crop")

##########################################################################################

import os
import os.path
import sys
import nuke
import time
#import addgeotab
import addrangetab

import autowrite
#import batchMOVs
#import changeFootagePath
import ChangeMissingFrame
import customNode
import diskcache
import glt_reloadRange
import mocha_import
import nodecount
import nodeOps
#import nukeprocess
#import papiTools
import production_presets
#import readwrites
import reloadallreads
import replaceChecker



#MULTI PLATFORM FIX CODE FOR WINDOWS OSX LINUX HYBRID SETUPS
#if sys.platform == 'darwin':
#	nuke.addFavoriteDir('Isilon', '/Volumes/optimus')
#else:
#	nuke.addFavoriteDir('Optimus', '//optimus.render.domain.server/optimus')
#use above to setup for multiple nuke version environment

#toolbar = nuke.menu('Nodes')

#import subprocess
#m=menubar.addMenu("Footage")
#rv version, but only one license so lets try djv
#m.addCommand('BrokenGlass rv', "subprocess.Popen('/usr/local/tweaks/rv/bin/rv /projects01/earthquake/global/review/03-08-2010/elements/BrokenGlass/', shell = True)")
#m.addCommand('Debris rv', "subprocess.Popen('/usr/local/tweaks/rv//bin/rv /projects01/earthquake/global/review/03-08-2010/elements/Debris/', shell = True)")
#m.addCommand('Dust rv', "subprocess.Popen('/usr/local/tweaks/rv/bin/rv /projects01/earthquake/global/review/03-08-2010/elements/Dust/', shell = True)")
#m.addCommand('FallingItems rv', "subprocess.Popen('/usr/local/tweaks/rv/bin/rv /projects01/earthquake/global/review/03-08-2010/elements/FallingItems/', shell = True)")
#m.addCommand('Smoke rv', "subprocess.Popen('/usr/local/tweaks/rv/bin/rv /projects01/earthquake/global/review/03-08-2010/elements/Smoke/', shell = True)")
#m.addCommand("-", "", "")#this command just adds a separation line in a dropdown

#mplayer version because thats the only other option we have and djv can't play multiple shots
#m.addCommand('BrokenGlass Mplayer', "subprocess.Popen('gmplayer /projects01/earthquake/global/review/03-08-2010/elements/BrokenGlass/*', shell = True)")
#m.addCommand('Debris mplayer', "subprocess.Popen('/usr/bin/gmplayer /projects01/earthquake/global/review/03-08-2010/elements/Debris/*', shell = True)")
#m.addCommand('Dust mplayer', "subprocess.Popen('/usr/bin/gmplayer /projects01/earthquake/global/review/03-08-2010/elements/Dust//*', shell = True)")
#m.addCommand('FallingItems mplayer', "subprocess.Popen('/usr/bin/gmplayer /projects01/earthquake/global/review/03-08-2010/elements/FallingItems/*', shell = True)")
#m.addCommand('Smoke mplayer', "subprocess.Popen('/usr/bin/gmplayer /projects01/earthquake/global/review/03-08-2010/elements//Smoke/*', shell = True)")
#djv version
#djv sucks because it can't string together a bunch of movie files to play, so I would have to write a playlist in python, bleh, will do this later
#m=menubar.addMenu("Footage djv")
#m.addCommand('0001_BrokenGlass', "os.popen('//usr//bin//djv_view -file_cache False //projects01//earthquake//global//review//03-08-2010//elements//BrokenGlass//0001_Glass_Break.mov')")

##########################################################################################

#setup menu variables
menuNo=nuke.menu("Nodes")

##########################################################################################
mim=menuNo.addMenu("Image")
# The "Image" menu
import makewritefromread
import sequencer
mim.addCommand("ReadWrite", 'makewritefromread.make_write_from_read()', 'ctrl+r', index=2)
mim.addCommand("colorNoise", "nuke.createNode('ColorNoise')", index=3)
mim.addCommand("Grad", "nuke.createNode('grad')", icon='grad.png', index=8)#add me
mim.addCommand("Ramper 2", "nuke.createNode('Ramper2')", index=9)
mim.addCommand("Sequencer", "sequencer.sequencer()", index=10)


##########################################################################################
mdr=menuNo.addMenu("Draw")
# The "Draw" menu

mdr.addCommand("Bezier Old", "nuke.createNode('Bezier')", 'alt+p', index=3) #adds old Bezier node back and modified to have addgeotab
mdr.addCommand("deWrinkler", "nuke.createNode('deWrinkler')", index=4)
mdr.addCommand('HealBrush', 'nuke.nodes.HealBrush()', index=8)
mdr.addCommand("FengGlow", "nuke.createNode('FengGlow')", index=8)
mdr.addCommand("FlareFactory Plus", "nuke.createNode(\"FlareFactory_Plus\")", icon="FlareFactoryPlus.png", index=8)

mdr.addCommand("Vignette2", "nuke.createNode('H_Vignette2')")
#mdr.addCommand("ZFaker", "nuke.createNode('H_ZFaker')")


#mbar=nuke.menu("Nuke")

def toggleMatterMode(arg):
  if arg==0:
    for n in nuke.allNodes('Matter'):
      n['remove_alpha'].execute()
  else:
    for n in nuke.allNodes('Matter'):
      n['add_alpha'].execute()

 

# Matter Menu
mdr.addCommand("Matter", "nuke.createNode('Matter')", index=8)
mdr.addCommand("Remove Matte", "toggleMatterMode(0)", "#+q")
mdr.addCommand("Add Matte", "toggleMatterMode(1)", "#+a")

#m = mbar.addMenu("&Matter")
#m.addCommand("Matter Gizmo", "nuke.tcl('Matter')", "#+p")
#m.addCommand("Remove Matte", "toggleMatterMode(0)", "#+q")
#m.addCommand("Add Matte", "toggleMatterMode(1)", "#+a")

##########################################################################################
mti=menuNo.addMenu("Time")

# The "Time" menu
import AssembleEdit
import holdFrames
mti.addCommand('AssembleEdit', 'AssembleEdit.AssembleEdit()', icon="AssEdit.png", index=3)#add me
mti.addCommand("dFielder", "nuke.createNode('dFielder')", index=4)
mti.addCommand('Hold Frames', 'holdFrames.holdFrames( nuke.selectedNode(), holdRange="all" )', index=8)
#mti.addCommand("Inverse Telecine", "nuke.createNode(\"InvTelecine\")", icon="Remove32.png", index=8)
#mti.addCommand("Telecine", "nuke.createNode(\"Telecine\")", icon="Add32.png", index=11)

##########################################################################################
mch=menuNo.addMenu("Channel")

# The Channel menu
import branchout
mch.addCommand("Branch Out Channels", "branchout.branchout()")

##########################################################################################
mco=menuNo.addMenu("Color")

# The Color menu
#nuke.load('/Users/deke/dev/OpenColorIO/build/src/nuke/OCIOColorSpace.so') 
#nuke.load('/Users/deke/dev/OpenColorIO/build/src/nuke/OCIODisplay.so') 
mco.addCommand("HighPass", "nuke.createNode(\"HighPass\")", icon="HighPass.png", index=11)
#import J_Ops
#mco.addCommand("J_3Way", "J_Ops.createNode(\"J_3Way\")", index=14)
#mco.addCommand("J_MergeHDR", "J_Ops.createNode(\"J_MergeHDR\")", index=15)
#mco.addCommand("J_Scopes", "J_Ops.createNode(\"J_Scopes\")", index=16)
#mco.addCommand("J_Ops Help", "J_Ops.launchHelp()", index=17)
mco.addCommand("KPGain", "nuke.createNode(\"KPGain\")", index=20)
mco.addCommand("MatchGrade", "nuke.createNode('MatchGrade')", index=24)
mco.addCommand("Slice Tool", "nuke.createNode('SliceTool')", index=30)
#mco.addCommand("OCIOColorSpace", "nuke.createNode(\"OCIOColorSpace\")", index=18)#need to recompile for n63
#mco.addCommand("OCIODisplay", "nuke.createNode(\"OCIODisplay\")", index=18)#need to recompile for n63

##########################################################################################
mfi=menuNo.addMenu("Filter")

# The "Filter" menu
import iFilter03
#mfi.addCommand("akromatism_stRub", "nuke.createNode('akromatism_stRub')")
#mfi.addCommand("alphaEdge", "nuke.createNode('alphaEdge')")
#mfi.addCommand("ChromAbb", "nuke.createNode('ChromAbb')")
#mfi.addCommand("degrainFB", "nuke.createNode('degrainFB')")
#mfi.addCommand("&Easy_LM2DMV", "nuke.createNode('Easy_LM2DMV')") #for handeling lm2dmv motion vectors which normally are made for Reelsmart MBlur
mfi.addCommand("FFT", "nuke.createNode('FFT')", index=16)#unhide unsupported built in tool
mfi.addCommand("FFT Multiply", "nuke.createNode('FFTMultiply')", index=17)#unhide unsupported built in tool
mfi.addCommand("Inverse FFT", "nuke.createNode('InvFFT')", index=18)#unhide unsupported built in tool
mfi.addCommand("iDilateErode", "nuke.createNode('iDilateErode')", index=19)
mfi.addCommand ('iFilter', 'nuke.nodes.iFilter(), iFilter03.iFilterCreate()', icon = "Constant.png", index=20)
#mfi.addCommand("&LM_2DMV", "nuke.createNode('LM_2DMV')") #for handeling lm2dmv motion vectors which normally are made for Reelsmart MBlur
mfi.addCommand("LensKernelFFT", "nuke.createNode('LensKernelFFT_v01')", index=21)
mfi.addCommand("Matte Edge", "nuke.createNode('matte_edge')", index=22)
#mfi.addCommand("Shartifact", "nuke.createNode('Shartifact')")
#mfi.addCommand("SoftErode", "nuke.createNode('SoftErode')")
#mfi.addCommand("Streaks", "nuke.createNode('H_Streaks')")
mfi.addCommand("StereoFake", "nuke.createNode('stereofake')")


##########################################################################################
mke=menuNo.addMenu("Keyer")

# The "Keyer" menu
mke.addCommand("DeSpilla", "nuke.createNode('DeSpilla')")
mke.addCommand("iDMattePro", "nuke.createNode('iDMattePro')")

##########################################################################################
mme=menuNo.addMenu("Merge")

# The "Merge" menu
mme.addCommand("AE Premult", "nuke.createNode('aePremult')", index=1)

##########################################################################################
mtr=menuNo.addMenu("Transform")

# The "Transform" menu
import im_cornerPin #giving error, must fix
#nuke.load ("CornerPin2DPY.py")

mtr.addCommand("AutoCrop", "nukescripts.autocrop()", icon="autocrop.xpm", index=2)#unhide built in tool
mtr.addCommand("Cam Quake!", "nuke.createNode(\"CamQuake\")", icon="CamQuake.png", index=5)
#mtr.addCommand("Glass", "nuke.createNode('Glass')", index=8)
mtr.addCommand("Ripple Distortion", "nuke.createNode('RippleDistortion')", index=18)
mtr.addCommand("Tracker 3D to 2D", "nuke.createNode(\"Tracker3Dto2D\")", icon="tracker3Dto2D.png", index=24)
mtr.addCommand("Turbulate", "nuke.createNode('turbulate')", index=28)
mtr.addCommand("Wave Distortion", "nuke.createNode('WaveDistortion')", index=31)
#mtr.addCommand( "CornerPin", "nuke.createNode('CornerPin2D', 'addUserKnob {20 values} addUserKnob {26 "" l Copy_and_set} addUserKnob {22 from--->to T ''CornerPin2DPY(0)'' +STARTLINE} addUserKnob {22 to--->from T ''CornerPin2DPY(1)''} addUserKnob {26 "" l Copy_from +STARTLINE} addUserKnob {22 from T ''CornerPin2DPY(3)'' +STARTLINE} addUserKnob {22 to T ''CornerPin2DPY(4)''} addUserKnob {26 "" l Paste_to +STARTLINE} addUserKnob {22 from T ''CornerPin2DPY(5)'' +STARTLINE} addUserKnob {22 to T ''CornerPin2DPY(6)''} addUserKnob {26 "" l Invert +STARTLINE} addUserKnob {22 invert T ''CornerPin2DPY(2)'' +STARTLINE} addUserKnob {26 "" l Set_key +STARTLINE} addUserKnob {22 from T ''CornerPin2DPY(7)'' +STARTLINE} addUserKnob {22 to T ''CornerPin2DPY(8)''} addUserKnob {26 "" l Info} addUserKnob {1 in_buffer} addUserKnob {3 varCopy INVISIBLE} addUserKnob {12 buf1 INVISIBLE} addUserKnob {12 buf2 INVISIBLE} addUserKnob {12 buf3 INVISIBLE} addUserKnob {12 buf4 INVISIBLE}', True)", icon = "CornerPin.png");
#don't need this anymore, cornerpin in 6.3 has copy to/from knobs now

#nuke.addOnUserCreate(im_cornerPin.cornerPin, nodeClass = 'CornerPin2D')
#nuke.addKnobChanged(im_cornerPin.cornerPinCB, nodeClass = 'CornerPin2D')

##########################################################################################
m3d=menuNo.addMenu("3D")

# The 3d menu
import addconstraintab
import panAndTile
#import TargetCamera

m3d.addCommand("CopyGeo", "nuke.createNode('CopyGeo')")
m3d.addCommand("Duplicator", "nuke.createNode('Duplicator')")
#nuke.menu("Nodes").addCommand("3D/Duplicate Geo", "DuplicateGeometry.DuplicateGeometry()") #not working at the moment, diagnose later
#m3d.addCommand("ImagePlane", "nuke.createNode('ImagePlane')") # broken at the moment, gives error - Obsolete_knob import_chan call is wrong, probably a missing NULL for script argument
m3d.addCommand('Pan And Tile', 'panAndTile.panAndTile()')
#m3d.addCommand('Point Projection', 'papiTools.PointProjection()' , icon='pointProjection.png')
m3d.addCommand("Projector", "nuke.createNode('Projector')")
m3d.addCommand('Position To Points', 'nuke.createNode("PositionToPoints")')#unhide unsupported built in tool
m3d.addCommand('ReLight', 'nuke.createNode("ReLight")')#unhide unsupported built in tool

#nuke.menu("Nodes").addCommand("3D/Geometry/ReadGeoPlus", "nuke.createNode('ReadGeoPlus')")
#nuke.menu("Nodes").addMenu("3D").addCommand("Target Camera", "TargetCamera.TargetCamera()") don't really need this right now
#nuke.menu("Nodes").addCommand("3D/Geometry/ReadGeo", "nuke.nodes.ReadGeo2();nuke.tcl('VCard');nuke.selectedNode().knob('display').setFlag(0)") #modify readGeo to have vcard

#set 3d defaults here
menuNo.addCommand("3D/Camera", "nuke.createNode('Camera2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify camera to have Add Constrain Tab
menuNo.addCommand("3D/Axis", "nuke.createNode('Axis2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify camera to have Add Constrain Tab
menuNo.addCommand("3D/Geometry/Card", "nuke.createNode('Card2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Card to have Add Constrain Tab
menuNo.addCommand("3D/Geometry/Cube", "nuke.createNode('Cube');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Cube to have Add Constrain Tab
menuNo.addCommand("3D/Geometry/Cylinder", "nuke.createNode('Cylinder');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Cylinder to have Add Constrain Tab
menuNo.addCommand("3D/Lights/Light", "nuke.createNode('Light2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Light to have Add Constrain Tab
menuNo.addCommand("3D/Lights/Direct", "nuke.createNode('DirectLight');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify DirectLight to have Add Constrain Tab
menuNo.addCommand("3D/Lights/Spotlight", "nuke.createNode('Spotlight');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Spotlight to have Add Constrain Tab

##########################################################################################
mve=menuNo.addMenu("Views")

#Views > Stereo Menu
menuNo.addCommand("Views/Stereo/Interleaver", "nuke.createNode('StereoInterleaver')")

##########################################################################################
mmd=menuNo.addMenu("MetaData")

#Metadata
#menubar=nuke.menu("Node Graph")
#import nuke

# Show MetaData Window
def showMeta():
  metakeys = nuke.thisNode().metadata().keys()
  metavalues = nuke.thisNode().metadata().values()
  metaData = ''
  numKeys = len(metakeys)
  for i in range(numKeys):
    metaData = metaData + metakeys[i] + ': ' + str(metavalues[i]) + '\n'
  return metaData
#m = menubar.addMenu("MetaData")
mmd.addCommand("Show MetaData","nuke.display('showMeta()', nuke.selectedNode(),'MetaData at ' + nuke.selectedNode().name(), 1000)","ctrl+m")


##########################################################################################
mot=menuNo.addMenu("Other")

# The "Other" menu
import autoBackup
import autobackdropRandomColor
import bakeGizmos
import dupReadDestroy
#import enableMultipleNodes
import fixPaths
import missingFrames
import PasteToSelected
#import SetSelectedValue

#mot.addCommand('Backdrop', 'nukescripts.autobackdrop()', 'alt+b', icon="Backdrop.png")#this is now built into nuke so I'm just assigning a hotkey to it
mot.addCommand('Backdrop', 'autobackdropRandomColor.autobackdropRandomColor()', 'alt+b', icon="Backdrop.png")#this is now built into nuke so I'm just assigning a hotkey to it
mot.addCommand('BakeGizmos', "bakeGizmos.bakeGizmos()")
#mot.addCommand("Auto Connect Node", "nuke.tcl(\"AutoConnectNode\")")#this needs node type defined first which used to just find all in script, so maybe something changed in 5.2 or 6.
#mot.addCommand("Batch MOVs", "batchMOVs.batchMOVs()")#haven't managed to get this to work yet
mot.addCommand("SideBySide Compare", "nuke.createNode('cSideBySide')")
#mot.addCommand("dpxInfo", "nuke.tcl(\"dpxInfo\")")#don't really need this anymore since viewMetaData now exists
#mot.addCommand("Enable Multiple Nodes", "enableMultipleNodes.enableMultipleNodes()")#enables all defocus/blurs, for speeding up scripts
#nuke.menu("Nodes").addMenu("Other").addCommand('Expression Manager', "nuke.tcl(\"ExpressionManager\")", "Alt+Shift+V")#this needs node type defined first which used to just find all in script, so maybe something changed in 5.2 or 6.
mot.addCommand('Fix Paths', 'fixPaths.fixPaths()')#this automates finding red nodes and fixing the paths to plates/geo that has moved
#mo.addCommand("J_Scopes", "nuke.tcl(\"J_Scopes\")")#this is a plugin, need to get newest compiled version of Jack's scopes
mot.addCommand("Missing Frames", "missingFrames.missingFrames()", 'alt+m')
mot.addCommand("Nuke Collect", "NukeCollect.collectThisComp()")
nuke.menu("Nodes").addMenu("Other").addCommand('Paste to Selected', 'PasteToSelected()', "Alt+Shift+V")
mot.addCommand("Reload All Reads", "reloadallreads.reloadallreads()", 'alt+shift+r')
mot.addCommand("Remove Dupe Read", "dupReadDestroy.dupReadDestroy()") # Call function on all nodes
#mo.addCommand("Remove Dupe Read", "dupReadDestroy.dupReadDestroy(True)") # Call function on selected nodes
#mo.addCommand("SetSelectedValue", "SetSelectedValue.SetSelectedValue()")#doesn't work right now
#mo.addCommand("Single Frame Render", "singleFrameRender.singleFrameRender()")#doesn't work right now

##########################################################################################

# The "Utils" submenu
mot.addCommand("Utils/Archive Script", "nuke.tcl(\"archivescript\")")
mot.addCommand("Utils/Auto Backup", "autoBackup.autoBackup()")
#mot.addCommand("Utils/aspectMCG", "nuke.createNode('aspectMCG')")
#mot.addCommand("Utils/AutoCompV4", "nuke.createNode('AutoCompV4')")#cool experiment but not very useful
#mot.addCommand("Utils/Get Timecode", "nuke.tcl(\"get_timecode\")")#says something about "get_timecode customstart" and then you do that and it errors "syntax error in expression "1001 + (customstart-1)": variable references require preceding $"
mot.addCommand("Utils/Guides", "nuke.createNode('Guides')")#both guides are missing stuff the other doesn't have, need to write one that combines the two
mot.addCommand("Utils/Guides2", "nuke.createNode('Guides2')")#both guides are missing stuff the other doesn't have, need to write one that combines the two
#mot.addCommand("Utils/Loupe", "nuke.createNode('loupe')")#just a cheesy loupe like in aperture
#mot.addCommand("Utils/moggaCropNSlate", "nuke.createNode('moggaCropNSlate')")
#mot.addCommand("Utils/moggaDFchild", "nuke.createNode('moggaDFchild')")
#mot.addCommand("Utils/moggaDFmaster", "nuke.createNode('moggaDFmaster')")
#mot.addCommand("Utils/moggaLens", "nuke.createNode('moggaLens')")
mot.addCommand("Utils/Replace Checker", "replaceChecker.readToChecker()")
#mot.addCommand("Utils/ReLighting", "nuke.createNode('ReLighting')")
#mot.addCommand("Utils/Relighting Old", "nuke.createNode('relighting.old')")
#mot.addCommand("Utils/SH Relighter", "nuke.createNode('SH_Relighter_v01')")
mot.addCommand("Utils/TimeCode Generator", "nuke.createNode('TCGen')")
mot.addCommand("Utils/TrigOps", "nuke.createNode('TrigOps')")


##########################################################################################
menuNk=nuke.menu("Nuke")

##########################################################################################
nfi=menuNk.addMenu("File")

#File Menu
import SourceGeoFolder
#nuke.toolbar('Nodes',).addCommand('RevealInFinder','revealInOS.revealInOS()')
nfi.addCommand('RevealInFinder','revealInOS.revealInOS()', index=8)#reveal in OS
nfi.addCommand("Import Geo Folder", "SourceGeoFolder.SourceGeoFolder()", index=7)


##########################################################################################
ned=menuNk.addMenu("Edit")

#Edit Menu
import renamenodes
menuNk.addCommand("Edit/Rename Nodes", "renamenodes.renamenodes()", 'F2', index=1 )

#howard & diogo's cool bookmarks
#later put these in the top menu
import bookmarker
menuNk.addCommand('Edit/Bookmarks/add Bookmark', 'bookmarker.bookmarkthis()', 'F3',icon='bookmark.png')
menuNk.addCommand('Edit/Bookmarks/find Bookmark', 'bookmarker.listbookmarks()', 'F4',icon='findBookmarks.png')
menuNk.addCommand('Edit/Bookmarks/cycle Bookmarks', 'bookmarker.cyclebookmarks()', 'F5',icon='cycleBookmarks.png' )

#shake clone
import nShakeClone
#molTools.addCommand( 'Shake Style Clone', 'shakeClone()', "Alt+v")
ned.addCommand( 'CloneE', 'nShakeClone.shakeClone()', "Alt+v", index=14)

#add a bunch of things to the Edit>Nodes menu

#Also adding a Node Menu at the top bar because there is lots of burried goodness in there that people are missing
#Also reorganizing and removing stuff I don't need
import nodeMenu
nuke.menu("Nuke").addMenu('Node/Align', index=1)

#franks align nodes in x or y
import alignNodes
menuNk.addCommand('Node/Align/Horizontal', 'alignNodes.alignNodes( nuke.selectedNodes(), direction="x" )', 'alt+x')
menuNk.addCommand('Node/Align/Vertical', 'alignNodes.alignNodes( nuke.selectedNodes(), direction="y" )', 'alt+y')

import Dots
menuNk.addCommand('Node/Align/Auto Dots', 'Dots.Dots()')

import Ym_alignNodes
menuNk.addCommand('Node/Align/Left X', 'Ym_alignNodes.alignLX()')
menuNk.addCommand('Node/Align/Center X', 'Ym_alignNodes.alignCX()')
menuNk.addCommand('Node/Align/Right X', 'Ym_alignNodes.alignRX()')
menuNk.addCommand('Node/Align/Interval X', 'Ym_alignNodes.align_intX()')

menuNk.addCommand('Node/Align/Top Y', 'Ym_alignNodes.alignTY()')
menuNk.addCommand('Node/Align/Center Y', 'Ym_alignNodes.alignCY()')
menuNk.addCommand('Node/Align/Under Y', 'Ym_alignNodes.alignUY()')
menuNk.addCommand('Node/Align/Interval Y', 'Ym_alignNodes.align_intY()')

menuNk.addCommand('Node/Align/Interval XX', 'Ym_alignNodes.align_intXX()')
menuNk.addCommand('Node/Align/Interval YY', 'Ym_alignNodes.align_intYY()')

import mirrorNodes
menuNk.addCommand('Node/Align/Mirror Horiz', 'mirrorNodes.mirrorNodes( nuke.selectedNodes(), direction="x" )', 'alt+ctrl+x')
menuNk.addCommand('Node/Align/Mirror Vert', 'mirrorNodes.mirrorNodes( nuke.selectedNodes(), direction="y" )', 'alt+ctrl+y')

#frank's node scale up trick
import scaleNodes
menuNk.addCommand('Node/Align/Scale Up', 'scaleNodes.scaleNodes( 1.1 )', '=')
menuNk.addCommand('Node/Align/Scale Down', 'scaleNodes.scaleNodes( 0.9 )', '-')
menuNk.findItem('Node').addCommand('Toggle Viewer Pipes', 'nodeOps.toggleViewerPipes()', 'alt+t')
nuke.addOnScriptLoad(nodeOps.toggleViewerPipes)

#thumbnailer
menuNk.addCommand('Node/Thumbnailer', 'thumbnailer.thumbnailer()', 'shift+t')

# select a tracker and a bezier node and hit ctrl+t to auto link the two together
#only works with Bezier, so disabling for the moment till I get it to work with Rotopaint
#nuke.menu('Nuke').findItem('Edit/Node').addCommand("Transform/Connect2Tracker", "nuke.tcl(\"Connect2Tracker\")", 'ctrl+t') 
#menu "Transform/Connect2Tracker" "^t" Connect2Tracker

##########################################################################################

nla=menuNk.addMenu("Layout")

##########################################################################################

nvi=menuNk.addMenu("Viewer")

##########################################################################################

nre=menuNk.addMenu("Render")

# The Render Menu

#nre.addCommand("-", "", "")#this command just adds a separation line in a dropdown

#nuke.menu("Nuke").addMenu("Render").addCommand("Submit Nuke To Deadline", "nuke.tcl(\"SubmitNukeToDeadline\")", 'alt+d') #deadline render launcher

#nuke.menu("Nuke").addMenu("Render").addCommand("Open in NukeX", "subprocess.Popen('/Applications/Nuke6.1v2b6/Nuke6.1v2b6.app/Contents/MacOS/Nuke6.1v2b6 --nukex [value root.name]', shell = True)")


#nuke.scriptSave()
#if nuke.env['nukex']:
#       args = [nuke.env['ExecutablePath'], nuke.root().name()]
#else:
#       args = [nuke.env['ExecutablePath'], '--nukex', nuke.root().name()]
#subprocess.Popen(args)
#quit()

#example off list to launch script in nukex, not working at the moment, need to finish it
#import subprocess
#def runInNukeX():
#    args = [nuke.env['ExecutablePath'], '--nukex', nuke.root().name()]
#    subprocess.Popen(args)
#    quit()
#nuke.menu("Nuke").addMenu("Render").addCommand("Open in NukeX",  'runInNukeX.runInNukeX()')

#, shell = True  
    

#doesn't seem to work in 6.3 anymore, will investigate later.
#create folder in write if it is missing
#turned off because it doesn't work
#import nuke
#import os
#def create_nuke_dirs():
#  for node in nuke.allNodes('Write'):
#      infile = node['file'].value()
#      if not os.path.exists(os.path.dirname(infile)):
#         os.makedirs(os.path.dirname(infile))
#
#nuke.addBeforeRender(create_nuke_dirs)

##########################################################################################

nca=menuNk.addMenu("Cache")

##########################################################################################
nhe=menuNk.addMenu("Help")

# The Help Menu

nhe.addCommand("Creative Crash Nuke Downloads", "nuke.tcl(\"start \\\"http://www.creativecrash.com/nuke/downloads/\\\"\")")
nhe.addCommand("Creative Crash Nuke Tutorials", "nuke.tcl(\"start \\\"http://www.creativecrash.com/nuke/tutorials/\\\"\")")
nhe.addCommand("Vfxtalk Nuke Forum", "nuke.tcl(\"start \\\"http://www.vfxtalk.com/forum/nuke-foundry-f60.html\\\"\")")
nhe.addCommand("Vfxtalk Nuke Downloads", "nuke.tcl(\"start \\\"http://www.vfxtalk.com/forum/nuke-plugins-scripts-f124.html\\\"\")")
nhe.addCommand("Nukepedia", "nuke.tcl(\"start \\\"http://www.nukepedia.com\\\"\")")

##########################################################################################

man=nuke.menu("Animation");
man.addCommand("File/Import_IFFFSE", "nuke.tcl(\"import_ifffse\")")

##########################################################################################
nlut = nuke.root().knob('luts')
nview = nuke.ViewerProcess

#custom luts for root
#nlut.addCurve("sLog", "{pow(10.0, ((t - 0.616596 - 0.03) /0.432699)) - 0.037584}")
#nlut.addCurve("AlexaV3LogC", "{ (t > 0.1496582 ? pow(10.0, (t - 0.385537) / 0.2471896) : t / 0.9661776 - 0.04378604) * 0.18 - 0.00937677 }")

# ViewerProcess LUTs 
#nview.register("AlexaV3Rec709", nuke.createNode, ("Vectorfield","vfield_file /Users/deke/nukescripts/lut/AlexaV3_EI0800_WYSIWYG_EE_nuke1d.cube colorspaceIn AlexaV3LogC"))
nview.register("AlexaV3Rec709", nuke.createNode, ("Vectorfield","vfield_file /Users/deke/nukescripts/lut/AlexaV3_K1S1_LogC2Video_Rec709_EE_nuke3d.cube colorspaceIn AlexaV3LogC"))

##########################################################################################
#Custom python panels

#add frank's search and replace panels
import SearchReplacePanel
def addSRPanel():
	'''Run the panel script and add it as a tab into the pane it is called from'''
        srPanel = SearchReplacePanel.SearchReplacePanel()
        return srPanel.addToPane()
nuke.menu('Pane').addCommand('SearchReplace', addSRPanel, "ctrl+alt+s")#THIS LINE WILL ADD THE NEW ENTRY TO THE PANE MENU
nukescripts.registerPanel('com.ohufx.SearchReplace', addSRPanel)#THIS LINE WILL REGISTER THE PANEL SO IT CAN BE RESTORED WITH LAYOUTS

#add frank's icon panels
import IconPanel
def addIconPanel():
#    global iconPanel
    iconPanel = IconPanel.IconPanel()
    return iconPanel.addToPane()
nuke.menu('Pane').addCommand('Universal Icons', addIconPanel, "ctrl+alt+i")
nukescripts.registerPanel('com.ohufx.IconPanel', addIconPanel)

#frank's fovCalculator
import FovCalculator
def addFovCalc():
	fovCalc = FovCalculator.FovCalculator()
	return fovCalc.addToPane()
nuke.menu('Pane').addCommand('Fov Calculator', addFovCalc, "ctrl+alt+f")
nukescripts.registerPanel('com.ohufx.FovCalculator', addFovCalc)
#paneMenu = nuke.menu( 'Pane' )

##########################################################################################

#Default Node Values Overide
nuke.knobDefault('Grade.black_clamp','false')# this turns off black clamp on Grade nodes
nuke.knobDefault( 'Bezier.linear', 'true' )
nuke.knobDefault("Write.channels", "rgba")
nuke.knobDefault("Root.format", "HD")
nuke.knobDefault("Root.project.directory", "[file dirname [knob root.name]]")

#nuke.knobDefault("PlanarTracker.previewFeatures", "true") #as of alpha 2 this can break the planar tracker so I am turning it off
#nuke.knobDefault("PlanarTracker.display_tracks", "true") #as of alpha 2 this can break the planar tracker so I am turning it off

#set viewer defaults
nuke.knobDefault("Viewer.gl_lighting", "true")# turn on headlamp by default, yay!


#setup stereo views_colours  
#nuke.root().knob('setlr').execute()#not sure why this isn't working
#nuke.root().knob('views_colours').setValue(True)#not sure why this isn't working

#This sets up views by default
#TURNING THIS OFF TEMPORARILY, THIS WILL ADD LEFT RIGHT TO SCRIPTS WITH L R NAMED EYES AND YOU WILL HAVE 4 EYES.  
#Need to make a simpler create stereo button instead
#nuke.knobDefault("Root.views",'left #ff0000\nright #00ff00')
#nuke.knobDefault("Root.views_colours","1")

# this kills all viewers apon opening new script
def killViewers():
    for v in nuke.allNodes("Viewer"):
        nuke.delete(v)
nuke.addOnScriptLoad(killViewers)

#flameConnect
menuNk.addCommand ('flameConnect', 'flameConnect.testen()', ' +y')

#ant's nodeVar
# Select a node, press Alt+Shift+n to assign your selected node to the Variable 'n' in the local context
#menubar=nuke.menu("Node Graph")
#m = menubar.addMenu("&Coding") 
#menubar=nuke.menu("Node Graph")
#m.addCommand("n = selectedNode","n = nuke.selectedNode()",'#+n')

import goToPlus #name of the package where goToPlus.py is installed 
nukescripts.goto_frame = goToPlus.goToPlus

#nuke.knobDefault("Text.font",nuke.defaultFontPathname())#[python {nuke.defaultFontPathname()}]

##########################################################################################

#My Presets for different nodes
if ( nuke.NUKE_VERSION_MAJOR >= 6) and ( nuke.NUKE_VERSION_MINOR >= 3 ): 
	import cam_presets
	cam_presets.nodePresetCamera()
	import reformat_presets
	reformat_presets.nodePresetReformat()