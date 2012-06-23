#Menu.py
# Author: 
# Deke Kincaid
# The Foundry
#
# 12/9/11
#
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
import psd2
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
toolbar=nuke.menu("Nodes")

##########################################################################################
m=toolbar.addMenu("Image")
# The "Image" menu
import makewritefromread
import sequencer
#import readFromWrite
import revealInOS

m.addCommand('Reveal In Finder','revealInOS.revealInOS()', icon='Read.png', index=1)#reveal in OS
m.addCommand('Read Folder', "nuke.load('recursiveLoad'), recursiveLoad()",  'alt+r', icon='Read.png', index=2)
m.addCommand("ReadList", 'readList.makereadList', index=3)
#m.addCommand('Read from Write', 'readFromWrite.readFromWrite()', icon='Read.png', 'shift+r', index=3) #not working, giving error SyntaxError: non-keyword arg after keyword arg
#m.addCommand('Write from Read', 'makewritefromread.make_write_from_read()', icon='Write.png', 'ctrl+r', index=3)

m.addCommand("Sequencer", "sequencer.sequencer()", index=11)





##########################################################################################
m=toolbar.addMenu("Draw")
# The "Draw" menu
import readList
import TX_Ramp

m.addCommand('3D Mattes', "nuke.createNode('Mattes3D')", index=0)
m.addCommand('Bezier Old', "nuke.createNode('Bezier')", 'alt+p', index=3) #adds old Bezier node back and modified to have addgeotab
m.addCommand('Color Noise', "nuke.createNode('ColorNoise')", index=4)

m.addCommand('DeWrinkler', "nuke.createNode('deWrinkler')", index=5)
m.addCommand('dGrad', "nuke.createNode('dGrad')", icon='grad.png', index=6)
m.addCommand("Flare Factory Plus", "nuke.createNode(\"FlareFactory_Plus\")", icon="FlareFactoryPlus.png", index=11)
m.addCommand("Feng Glow", "nuke.createNode('FengGlow')", index=12)
m.addCommand('Grad', "nuke.createNode('grad')", icon='grad.png', index=13)
m.addCommand('Heal Brush', 'nuke.nodes.HealBrush()', index=17)
m.addCommand('Linear Ramp', "nuke.createNode('L_Ramp_v01')", icon='Ramp.png', index=21)
m.addCommand('Magic Carpet', "nuke.createNode('magicCarpet')", icon='magicCarpet.png', index=22)
m.addCommand('P Ramp', "nuke.createNode('P_Ramp')", icon='Ramp.png', index=25)
m.addCommand('pPass Mask', "nuke.createNode('PP_Mask_hub_V2')", index=26)
m.addCommand('Point Position Mask', "nuke.createNode('PointPositionMask')", index=27)
m.addCommand('Ramper', "nuke.createNode('Ramper2')", icon='Ramp.png', index=28)
m.addCommand('Ramp Remap', "nuke.createNode('RampMap')", icon='Ramp.png', index=29)
m.addCommand('TX Ramp', "nuke.createNode('TX_Ramp')", icon='Ramp.png')
m.addCommand("Vignette", "nuke.createNode('H_Vignette2')")
#m.addCommand("ZFaker", "nuke.createNode('H_ZFaker')")


#mbar=nuke.menu("Nuke")

#def toggleMatterMode(arg):
#  if arg==0:
#    for n in nuke.allNodes('Matter'):
#      n['remove_alpha'].execute()
#  else:
#    for n in nuke.allNodes('Matter'):
#      n['add_alpha'].execute()

 

# Matter Menu
#m.addCommand("Matter", "nuke.createNode('Matter')", index=18)
#m.addCommand("Remove Matte", "toggleMatterMode(0)", "#+q", index=19)
#m.addCommand("Add Matte", "toggleMatterMode(1)", "#+a", index=20)

##########################################################################################
m=toolbar.addMenu("Time")

# The "Time" menu
import AssembleEdit
import holdFrames
m.addCommand('AssembleEdit', 'AssembleEdit.AssembleEdit()', icon="AssEdit.png", index=3)#add me
m.addCommand("dFielder", "nuke.createNode('dFielder')", index=4)
m.addCommand('Hold Frames', 'holdFrames.holdFrames( nuke.selectedNode(), holdRange="all" )', index=8)
#m.addCommand("Inverse Telecine", "nuke.createNode(\"InvTelecine\")", icon="Remove32.png", index=8)
#m.addCommand("Telecine", "nuke.createNode(\"Telecine\")", icon="Add32.png", index=11)

##########################################################################################
m=toolbar.addMenu("Channel")

# The Channel menu
import branchout
m.addCommand("Branch Out Channels", "branchout.branchout()", index=0)

##########################################################################################
m=toolbar.addMenu("Color")

# The Color menu
m.addCommand("HighPass", "nuke.createNode(\"HighPass\")", icon="HighPass.png", index=11)
#import J_Ops
#m.addCommand("J_3Way", "J_Ops.createNode(\"J_3Way\")", index=14)
#m.addCommand("J_MergeHDR", "J_Ops.createNode(\"J_MergeHDR\")", index=15)
#m.addCommand("J_Scopes", "J_Ops.createNode(\"J_Scopes\")", index=16)
#m.addCommand("J_Ops Help", "J_Ops.launchHelp()", index=17)
m.addCommand("KPGain", "nuke.createNode(\"KPGain\")", index=20)
m.addCommand("MatchGrade", "nuke.createNode('MatchGrade')", index=24)
m.addCommand("Slice Tool", "nuke.createNode('SliceTool')", index=30)

##########################################################################################
m=toolbar.addMenu("Filter")

# The "Filter" menu
import iFilter03
#m.addCommand("akromatism_stRub", "nuke.createNode('akromatism_stRub')")
#m.addCommand("alphaEdge", "nuke.createNode('alphaEdge')")
#m.addCommand("ChromAbb", "nuke.createNode('ChromAbb')")
#m.addCommand("degrainFB", "nuke.createNode('degrainFB')")
#m.addCommand("&Easy_LM2DMV", "nuke.createNode('Easy_LM2DMV')") #for handeling lm2dmv motion vectors which normally are made for Reelsmart MBlur
m.addCommand("FFT", "nuke.createNode('FFT')", index=16)#unhide unsupported built in tool
m.addCommand("FFT Multiply", "nuke.createNode('FFTMultiply')", index=17)#unhide unsupported built in tool
m.addCommand("iDilateErode", "nuke.createNode('iDilateErode')", index=20)
m.addCommand ('iFilter', 'nuke.nodes.iFilter(), iFilter03.iFilter03()', icon = "Constant.png", index=21)
m.addCommand("Inverse FFT", "nuke.createNode('InvFFT')", index=22)#unhide unsupported built in tool
#m.addCommand("&LM_2DMV", "nuke.createNode('LM_2DMV')") #for handeling lm2dmv motion vectors which normally are made for Reelsmart MBlur
m.addCommand("LensKernelFFT", "nuke.createNode('LensKernelFFT_v01')", index=24)
#m.addCommand("Matte Edge", "nuke.createNode('matte_edge')", index=27)
#m.addCommand("Shartifact", "nuke.createNode('Shartifact')")
#m.addCommand("SoftErode", "nuke.createNode('SoftErode')")
#m.addCommand("Streaks", "nuke.createNode('H_Streaks')")
m.addCommand("StereoFake", "nuke.createNode('stereofake')", index=33)
m.addCommand("V_EdgeMatte", "nuke.createNode('V_EdgeMatte')", index=36)



##########################################################################################
m=toolbar.addMenu("Keyer")

# The "Keyer" menu
m.addCommand("DeSpilla", "nuke.createNode('DeSpilla')", index=0)
m.addCommand("iDMattePro", "nuke.createNode('iDMattePro')", index=5)

##########################################################################################
m=toolbar.addMenu("Merge")

# The "Merge" menu
m.addCommand("AE Premult", "nuke.createNode('aePremult')", index=1)

##########################################################################################
m=toolbar.addMenu("Transform")

# The "Transform" menu
import im_cornerPin #giving error, must fix
#nuke.load ("CornerPin2DPY.py")

m.addCommand("AutoCrop", "nukescripts.autocrop()", icon="autocrop.xpm", index=0)#unhide built in tool
m.addCommand("Cam Quake!", "nuke.createNode(\"CamQuake\")", icon="CamQuake.png", index=5)
#m.addCommand("Glass", "nuke.createNode('Glass')", index=8)
m.addCommand("Ripple Distortion", "nuke.createNode('RippleDistortion')", index=18)
m.addCommand("Tracker 3D to 2D", "nuke.createNode(\"Tracker3Dto2D\")", icon="tracker3Dto2D.png", index=24)
m.addCommand("Turbulate", "nuke.createNode('turbulate')", index=28)
m.addCommand("Wave Distortion", "nuke.createNode('WaveDistortion')", index=31)
#m.addCommand( "CornerPin", "nuke.createNode('CornerPin2D', 'addUserKnob {20 values} addUserKnob {26 "" l Copy_and_set} addUserKnob {22 from--->to T ''CornerPin2DPY(0)'' +STARTLINE} addUserKnob {22 to--->from T ''CornerPin2DPY(1)''} addUserKnob {26 "" l Copy_from +STARTLINE} addUserKnob {22 from T ''CornerPin2DPY(3)'' +STARTLINE} addUserKnob {22 to T ''CornerPin2DPY(4)''} addUserKnob {26 "" l Paste_to +STARTLINE} addUserKnob {22 from T ''CornerPin2DPY(5)'' +STARTLINE} addUserKnob {22 to T ''CornerPin2DPY(6)''} addUserKnob {26 "" l Invert +STARTLINE} addUserKnob {22 invert T ''CornerPin2DPY(2)'' +STARTLINE} addUserKnob {26 "" l Set_key +STARTLINE} addUserKnob {22 from T ''CornerPin2DPY(7)'' +STARTLINE} addUserKnob {22 to T ''CornerPin2DPY(8)''} addUserKnob {26 "" l Info} addUserKnob {1 in_buffer} addUserKnob {3 varCopy INVISIBLE} addUserKnob {12 buf1 INVISIBLE} addUserKnob {12 buf2 INVISIBLE} addUserKnob {12 buf3 INVISIBLE} addUserKnob {12 buf4 INVISIBLE}', True)", icon = "CornerPin.png");
#don't need this anymore, cornerpin in 6.3 has copy to/from knobs now

#nuke.addOnUserCreate(im_cornerPin.cornerPin, nodeClass = 'CornerPin2D')
#nuke.addKnobChanged(im_cornerPin.cornerPinCB, nodeClass = 'CornerPin2D')

##########################################################################################
m=toolbar.addMenu("3D")

# The 3d menu
import CopyCamForProj_v003_r01
import addconstraintab
import panAndTile
import SourceGeoFolder
#import TargetCamera
#import vrayCameraAttributes
#nuke.load('vrayCameraAttributes.py')

m.addCommand("CopyCam", "CopyCamForProj_v003_r01.copyCamForProj()", "Shift+v", index=1)
m.addCommand("CopyGeo", "nuke.createNode('CopyGeo')", index=2)
m.addCommand("Duplicator", "nuke.createNode('Duplicator')", index=3)
m.addCommand("EnvRelight", "nuke.createNode('EnvRelight')", index=4)
#nuke.menu("Nodes").addCommand("3D/Duplicate Geo", "DuplicateGeometry.DuplicateGeometry()") #not working at the moment, diagnose later
#m.addCommand("ImagePlane", "nuke.createNode('ImagePlane')") # broken at the moment, gives error - Obsolete_knob import_chan call is wrong, probably a missing NULL for script argument
m.addCommand('Pan And Tile', 'panAndTile.panAndTile()', index=13)
#m.addCommand('Point Projection', 'papiTools.PointProjection()' , icon='pointProjection.png')
m.addCommand("Projector", "nuke.createNode('Projector')", index=15)

m.addCommand("Geometry/ReadGeo Folder", "SourceGeoFolder.SourceGeoFolder()", icon='Read.png', index=8)

#m.addCommand("Geometry/ReadGeoPlus", "nuke.createNode('ReadGeoPlus')")
#m.addMenu("3D").addCommand("Target Camera", "TargetCamera.TargetCamera()") don't really need this right now
#m.addCommand("Geometry/ReadGeo", "nuke.nodes.ReadGeo2();nuke.tcl('VCard');nuke.selectedNode().knob('display').setFlag(0)") #modify readGeo to have vcard
if ( nuke.NUKE_VERSION_MAJOR <= 7):
	m.addCommand('ReLight', 'nuke.createNode("ReLight")', index=17)#unhide unsupported built in tool
	m.addCommand('Position To Points', 'nuke.createNode("PositionToPoints")', index=16)#unhide unsupported built in tool	


##########################################################################################
m=toolbar.addMenu("Views")

#Views > Stereo Menu
toolbar.addCommand("Views/Stereo/Interleaver", "nuke.createNode('StereoInterleaver')")

##########################################################################################
m=toolbar.addMenu("MetaData")

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
m.addCommand("Show MetaData","nuke.display('showMeta()', nuke.selectedNode(),'MetaData at ' + nuke.selectedNode().name(), 1000)","ctrl+m")


##########################################################################################
m=toolbar.addMenu("Other")

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
import writeChecker

m.addCommand("Archive Script", "nuke.tcl(\"archivescript\")", index=2 )
m.addCommand("Auto Backup", "autoBackup.autoBackup()", index=3 )
#m.addCommand("Auto Connect Node", "nuke.tcl(\"AutoConnectNode\")")#this needs node type defined first which used to just find all in script, so maybe something changed in 5.2 or 6.
m.addCommand('Backdrop', 'autobackdropRandomColor.autobackdropRandomColor()', 'alt+b', icon="Backdrop.png", index=4)#this is now built into nuke so I'm just assigning a hotkey to it
m.addCommand('BakeGizmos', "bakeGizmos.bakeGizmos()", index=5 )
#m.addCommand("Enable Multiple Nodes", "enableMultipleNodes.enableMultipleNodes()")#enables all defocus/blurs, for speeding up scripts
m.addCommand('Fix Paths', 'fixPaths.fixPaths()', index=8 )#this automates finding red nodes and fixing the paths to plates/geo that has moved
m.addCommand("Missing Frames", "missingFrames.missingFrames()", 'alt+m', index=10 )
m.addCommand("Nuke Collect", "NukeCollect.collectThisComp()", index=11 )
nuke.menu("Nodes").addMenu("Other").addCommand('Paste to Selected', 'PasteToSelected()', "Alt+Shift+V", index=14 )
m.addCommand("Replace Checker", "replaceChecker.readToChecker()" , index=16)
m.addCommand("Reload All Reads", "reloadallreads.reloadallreads()", 'alt+shift+r', index=16 )
m.addCommand("Remove Dupe Read", "dupReadDestroy.dupReadDestroy()", index=16 ) # Call function on all nodes
#m.addCommand("Remove Dupe Read", "dupReadDestroy.dupReadDestroy(True)") # Call function on selected nodes
#m.addCommand("SideBySide Compare", "nuke.createNode('cSideBySide')")
#m.addCommand("SetSelectedValue", "SetSelectedValue.SetSelectedValue()")#doesn't work right now
#m.addCommand("Single Frame Render", "singleFrameRender.singleFrameRender()")#doesn't work right now
m.addCommand("TimeCode Generator", "nuke.createNode('TCGen')" )
m.addCommand("TrigOps", "nuke.createNode('TrigOps')")
m.addCommand("writeChecker", "writeChecker.writeChecker()")




##########################################################################################

# The "Utils" submenu
#m.addCommand("Utils/Get Timecode", "nuke.tcl(\"get_timecode\")")#says something about "get_timecode customstart" and then you do that and it errors "syntax error in expression "1001 + (customstart-1)": variable references require preceding $"
#m.addCommand("Utils/Loupe", "nuke.createNode('loupe')")#just a cheesy loupe like in aperture
#m.addCommand("Utils/ReLighting", "nuke.createNode('ReLighting')")
#m.addCommand("Utils/Relighting Old", "nuke.createNode('relighting.old')")
#m.addCommand("Utils/SH Relighter", "nuke.createNode('SH_Relighter_v01')")


##########################################################################################
menubar=nuke.menu("Nuke")
#menubar=nuke.menu("Nuke")

##########################################################################################
m=menubar.addMenu("File")

#File Menu



##########################################################################################
m=menubar.addMenu("Edit")

#Edit Menu
import renamenodes
menubar.addCommand("Edit/Rename Nodes", "renamenodes.renamenodes()", 'F2', index=1 )

#howard & diogo's cool bookmarks
#later put these in the top menu
import bookmarker
menubar.addCommand('Edit/Bookmarks/add Bookmark', 'bookmarker.bookmarkthis()', 'F3',icon='bookmark.png')
menubar.addCommand('Edit/Bookmarks/find Bookmark', 'bookmarker.listbookmarks()', 'F4',icon='findBookmarks.png')
menubar.addCommand('Edit/Bookmarks/cycle Bookmarks', 'bookmarker.cyclebookmarks()', 'F5',icon='cycleBookmarks.png' )

#shake clone
import nShakeClone
#molTools.addCommand( 'Shake Style Clone', 'shakeClone()', "Alt+v")
m.addCommand( 'CloneE', 'nShakeClone.shakeClone()', "Alt+v", index=14)

#add a bunch of things to the Edit>Nodes menu

#Also adding a Node Menu at the top bar because there is lots of burried goodness in there that people are missing
#Also reorganizing and removing stuff I don't need
import nodeMenu
nuke.menu("Nuke").addMenu('Node/Align', index=1)

#franks align nodes in x or y
import alignNodes
menubar.addCommand('Node/Align/Horizontal', 'alignNodes.alignNodes( nuke.selectedNodes(), direction="x" )', 'alt+x')
menubar.addCommand('Node/Align/Vertical', 'alignNodes.alignNodes( nuke.selectedNodes(), direction="y" )', 'alt+y')

import convertGizmosToGroups
#nuke.menu('Nuke').findItem('Edit/Node')
menubar.addCommand('Node/Convert Gizmo to Group', 'convertGizmosToGroups.convertGizmosToGroups()', 'ctrl+alt+h')

import Dots
menubar.addCommand('Node/Align/Auto Dots', 'Dots.Dots()')

import Ym_alignNodes
menubar.addCommand('Node/Align/Left X', 'Ym_alignNodes.alignLX()')
menubar.addCommand('Node/Align/Center X', 'Ym_alignNodes.alignCX()')
menubar.addCommand('Node/Align/Right X', 'Ym_alignNodes.alignRX()')
menubar.addCommand('Node/Align/Interval X', 'Ym_alignNodes.align_intX()')

menubar.addCommand('Node/Align/Top Y', 'Ym_alignNodes.alignTY()')
menubar.addCommand('Node/Align/Center Y', 'Ym_alignNodes.alignCY()')
menubar.addCommand('Node/Align/Under Y', 'Ym_alignNodes.alignUY()')
menubar.addCommand('Node/Align/Interval Y', 'Ym_alignNodes.align_intY()')

menubar.addCommand('Node/Align/Interval XX', 'Ym_alignNodes.align_intXX()')
menubar.addCommand('Node/Align/Interval YY', 'Ym_alignNodes.align_intYY()')

import mirrorNodes
menubar.addCommand('Node/Align/Mirror Horiz', 'mirrorNodes.mirrorNodes( nuke.selectedNodes(), direction="x" )', 'alt+ctrl+x')
menubar.addCommand('Node/Align/Mirror Vert', 'mirrorNodes.mirrorNodes( nuke.selectedNodes(), direction="y" )', 'alt+ctrl+y')

#frank's node scale up trick
import scaleNodes
menubar.addCommand('Node/Align/Scale Up', 'scaleNodes.scaleNodes( 1.1 )', '=')
menubar.addCommand('Node/Align/Scale Down', 'scaleNodes.scaleNodes( 0.9 )', '-')
menubar.findItem('Node').addCommand('Toggle Viewer Pipes', 'nodeOps.toggleViewerPipes()', 'alt+t')
nuke.addOnScriptLoad(nodeOps.toggleViewerPipes)

#thumbnailer
menubar.addCommand('Node/Thumbnailer', 'thumbnailer.thumbnailer()', 'shift+t')

#version read nodes to latest
import versionToLatest
menubar.addCommand( 'Edit/Node/Filename/Version to Latest (Reads only)' , versionToLatest.versionToLatest)

# select a tracker and a bezier node and hit ctrl+t to auto link the two together
#only works with Bezier, so disabling for the moment till I get it to work with Rotopaint
#nuke.menu('Nuke').findItem('Edit/Node').addCommand("Transform/Connect2Tracker", "nuke.tcl(\"Connect2Tracker\")", 'ctrl+t') 
#menu "Transform/Connect2Tracker" "^t" Connect2Tracker

##########################################################################################

m=menubar.addMenu("Layout")

##########################################################################################

m=menubar.addMenu("Viewer")

##########################################################################################

m=menubar.addMenu("Render")

# The Render Menu

#m.addCommand("-", "", "")#this command just adds a separation line in a dropdown

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

#def createWriteDir(): #added from here: http://freelunch.dk/?p=220
#  import nuke, os
#  file = nuke.filename(nuke.thisNode())
#  dir = os.path.dirname( file )
#  osdir = nuke.callbacks.filenameFilter( dir )
#  os.makedirs( osdir )
#nuke.addBeforeRender(createWriteDir)

#taken from Bill Gilman post on nuke-users list and added on by Nathan Rusch
#def createWriteDirs():
#    import os
#    import re
#    baseDir = os.path.dirname(nuke.filename(nuke.thisNode()))
#    viewTokenRE = re.compile(r'%V')
#    if viewTokenRE.search(baseDir):
#        nodeViews = nuke.thisNode()['views'].value().split()
#        outDirs = [nuke.filenameFilter(viewTokenRE.sub(v, baseDir)) for v in nodeViews]
#    else:
#        outDirs = [nuke.filenameFilter(baseDir)]
#    for outDir in outDirs:
#        if not os.path.exists(outDir):
#            print 'Creating output directory: %s' % outDir
#            try:
#                os.makedirs(outDir)
#            except (OSError, IOError) e:
                # Don't choke if directory has been created since we checked.
                # This can be an issue with farm renders.
#                import errno
#                if e.errno != errno.EEXIST:
#                    raise
                 
#nuke.addBeforeRender(createWriteDir)


##########################################################################################
if ( nuke.NUKE_VERSION_MAJOR >= 6) and ( nuke.NUKE_VERSION_MINOR >= 3 ):#this gets rid of the cache menu from showing up in 6.2
	m=menubar.addMenu("Cache")

##########################################################################################
m=menubar.addMenu("Help")

# The Help Menu

m.addCommand("Creative Crash Nuke Downloads", "nuke.tcl(\"start \\\"http://www.creativecrash.com/nuke/downloads/\\\"\")")
m.addCommand("Creative Crash Nuke Tutorials", "nuke.tcl(\"start \\\"http://www.creativecrash.com/nuke/tutorials/\\\"\")")
m.addCommand("Vfxtalk Nuke Forum", "nuke.tcl(\"start \\\"http://www.vfxtalk.com/forum/nuke-foundry-f60.html\\\"\")")
m.addCommand("Vfxtalk Nuke Downloads", "nuke.tcl(\"start \\\"http://www.vfxtalk.com/forum/nuke-plugins-scripts-f124.html\\\"\")")
m.addCommand("Nukepedia", "nuke.tcl(\"start \\\"http://www.nukepedia.com\\\"\")")

##########################################################################################

m=nuke.menu("Animation");
m.addCommand("File/Import_IFFFSE", "nuke.tcl(\"import_ifffse\")")

##########################################################################################
nlut = nuke.root().knob('luts')
nview = nuke.ViewerProcess

#custom luts for root
if ( nuke.NUKE_VERSION_MAJOR >= 6) and ( nuke.NUKE_VERSION_MINOR <= 2 ): #only load slog and alexav3logc if using nuke 6.2 or earlier since these are included with 6.3
	nlut.addCurve("sLog", "{pow(10.0, ((t - 0.616596 - 0.03) /0.432699)) - 0.037584}")
	nlut.addCurve("AlexaV3LogC", "{ (t > 0.1496582 ? pow(10.0, (t - 0.385537) / 0.2471896) : t / 0.9661776 - 0.04378604) * 0.18 - 0.00937677 }")

# ViewerProcess LUTs 
#nview.register("AlexaV3Rec709", nuke.createNode, ("Vectorfield","vfield_file /Users/deke/nukescripts/lut/AlexaV3_EI0800_WYSIWYG_EE_nuke1d.cube colorspaceIn AlexaV3LogC"))
nview.register("AlexaV3Rec709", nuke.createNode, ("Vectorfield","vfield_file /Users/deke/nukescripts/lut/AlexaV3_K1S1_LogC2Video_Rec709_EE_nuke3d.cube colorspaceIn AlexaV3LogC"))

##########################################################################################
#Custom python panels
paneMenu = nuke.menu( 'Pane' )

#import reportABug
#def addRABPanel():
#    rabPanel = reportABug.reportABug()
#    return rabPanel.addToPane()
#paneMenu.addCommand('Report A Bug', addRABPanel, "ctrl+alt+b")
#nukescripts.registerPanel('com.deke.reportABug', addRABPanel)

#add frank's search and replace panels
import SearchReplacePanel
def addSRPanel():
        srPanel = SearchReplacePanel.SearchReplacePanel()
        return srPanel.addToPane()
paneMenu.addCommand('SearchReplace', addSRPanel, "ctrl+alt+s")#THIS LINE WILL ADD THE NEW ENTRY TO THE PANE MENU
nukescripts.registerPanel('com.ohufx.SearchReplace', addSRPanel)#THIS LINE WILL REGISTER THE PANEL SO IT CAN BE RESTORED WITH LAYOUTS

#add frank's icon panels
import IconPanel
def addIconPanel():
    global iconPanel
    iconPanel = IconPanel.IconPanel()
    return iconPanel.addToPane()
paneMenu.addCommand('Universal Icons', addIconPanel, "ctrl+alt+i")
nukescripts.registerPanel('com.ohufx.IconPanel', addIconPanel)

#frank's fovCalculator, not coming up for some reason, will investigate later
import FovCalculator
def addFovCalc():
	fovCalc = FovCalculator.FovCalculator()
	return fovCalc.addToPane()
paneMenu.addCommand('Fov Calculator', addFovCalc, "ctrl+alt+f" )
nukescripts.registerPanel('com.ohufx.FovCalculator', addFovCalc )


##########################################################################################

##################   Default Node Values Overide   ##################
nuke.knobDefault('Grade.black_clamp','false')# this turns off black clamp on Grade nodes
nuke.knobDefault( 'Bezier.linear', 'true' )


##################   WRITE NODE   ##################
nuke.knobDefault("Write.channels", "rgba")
nuke.knobDefault("Write.file_type","jpg") 
nuke.knobDefault("Write._jpeg_quality", "1")
nuke.knobDefault("Write._jpeg_sub_sampling", "1")
nuke.knobDefault('Write.beforeRender' , 'readList.updatereadList()')

##################   3D DEFAULTS   ##################
toolbar.addCommand("3D/Camera", "nuke.createNode('Camera2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify camera to have Add Constrain Tab
toolbar.addCommand("3D/Axis", "nuke.createNode('Axis2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify camera to have Add Constrain Tab
toolbar.addCommand("3D/Geometry/Card", "nuke.createNode('Card2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Card to have Add Constrain Tab
toolbar.addCommand("3D/Geometry/Cube", "nuke.createNode('Cube');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Cube to have Add Constrain Tab
toolbar.addCommand("3D/Geometry/Cylinder", "nuke.createNode('Cylinder');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Cylinder to have Add Constrain Tab
toolbar.addCommand("3D/Lights/Light", "nuke.createNode('Light2');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Light to have Add Constrain Tab
toolbar.addCommand("3D/Lights/Direct", "nuke.createNode('DirectLight');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify DirectLight to have Add Constrain Tab
toolbar.addCommand("3D/Lights/Spotlight", "nuke.createNode('Spotlight');addconstraintab.constrain();nuke.selectedNode().knob('display').setFlag(0)") #modify Spotlight to have Add Constrain Tab


##################   PROJECT SETTINGS   ##################
nuke.knobDefault("Root.format", "HD")
nuke.knobDefault("Root.project.directory", "[file dirname [knob root.name]]")       
               
# os.chdir(os.path.dirname(nuke.root().name())) # set this to onScriptLoad of the project setting to automatically set the working directory to where the nuke file is located

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
#if ( nuke.MACOS = True) or ( nuke.WIN32 = True ): #linux does not like flameConnect script and it adds weird stuff to the top menu, so turn it off with linux till I figure out why it is messed up
#	menubar.addCommand ('flameConnect', 'flameConnect.testen()', ' +y')
#ant's nodeVar
# Select a node, press Alt+Shift+n to assign your selected node to the Variable 'n' in the local context
#menubar=nuke.menu("Node Graph")
#m = menubar.addMenu("&Coding") 
#menubar=nuke.menu("Node Graph")
#m.addCommand("n = selectedNode","n = nuke.selectedNode()",'#+n')

import goToPlus #name of the package where goToPlus.py is installed 
nukescripts.goto_frame = goToPlus.goToPlus

#nuke.knobDefault("Text.font",nuke.defaultFontPathname())#[python {nuke.defaultFontPathname()}]

import nuke
import tabtabtab
m_edit = nuke.menu("Nuke").findItem("Edit")
m_edit.addCommand("Tabtabtab", tabtabtab.main, "Tab")

##########################################################################################
#Nuke to Mari knob defaults
                                      
#nuke.root().knob('socketPort').setValue(50008)
#nuke.root().knob('hostName').setValue('localhost')
#nuke.root().knob('mariDataDir').setValue('/tmp')
#mari.prefs.set('Scripts/Mari Command Port/port', 6105)
                       

###########################   NODE PRESETS   ########################### 

#adding presets for different nuke nodes
if ( nuke.NUKE_VERSION_MAJOR >= 6) and ( nuke.NUKE_VERSION_MINOR >= 3 ): 
	import cam_presets
	cam_presets.nodePresetCamera()
	import reformat_presets
	reformat_presets.nodePresetReformat()