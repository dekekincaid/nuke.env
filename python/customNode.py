# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
#
# An example of a custom write node

import nuke, os

########################################################################

def promptForJob():
  if not os.environ.get('JOB')  or not os.environ.get('SHOT'):
    ## only prompt if JOB and SHOT is not set in the environment
    p = nuke.Panel("Job System")
    p.addSingleLineInput("Show:", os.environ.get('JOB') )
    p.addSingleLineInput("Shot:",  os.environ.get('SHOT') )
    if p.show():
      os.environ['JOB'] = p.value( "Show:" )
      os.environ['SHOT'] = p.value( "Shot:" )


########################################################################
# customising the creation of nodes
#
# override nuke.createNode to return the custom write node
#
# it is possible to override nuke.nodes. as well.  See the user manual for an example.

nukeOriginalCreateNode = nuke.createNode

def attachCustomCreateNode():
  nuke.createNode = customCreateNode

def customCreateNode(node, knobs = "", inpanel = True):
  if node == "Write":
    writeNode = nukeOriginalCreateNode( node, knobs, inpanel )
    ## attach our custom tab
    createJobSystemTab( writeNode )
    return writeNode
  else:
    return nukeOriginalCreateNode( node, knobs, inpanel )
    
########################################################################

def createJobSystemTab(node):
	#### create knobs
	tabKnob = nuke.Tab_Knob('JobSystem')
	jobKnob = nuke.EvalString_Knob('job')
	shotKnob = nuke.EvalString_Knob('shot')
	versionKnob = nuke.Int_Knob('version')
	takeKnob = nuke.Int_Knob('take')
	labelKnob = nuke.EvalString_Knob('usr_label', 'label')
	extKnob = nuke.EvalString_Knob('ext')
	buttonKnob = nuke.PyScript_Knob('Create Ouptut')

	#### set some defaults for the knobs
	jobKnob.setValue(os.environ.get('JOB'))
	shotKnob.setValue(os.environ.get('SHOT'))
	versionKnob.setValue(1)
	takeKnob.setValue(1)
	labelKnob.setValue('look')
	extKnob.setValue('exr')

  #### the python script to run when the user presses the 'Create dirs' button
	script = """
job = nuke.thisNode()['job'].value()
shot = nuke.thisNode()['shot'].value()
version = nuke.thisNode()['version'].value()
take = nuke.thisNode()['take'].value()
label = nuke.thisNode()['usr_label'].value()
ext = nuke.thisNode()['ext'].value()
user = os.environ.get('USER')

#### build up the shot name
shotName = '%s_v%02d_%s_%s' % (shot, int(version), user, label)

#### grab base render directory from environment
baseDir = os.environ.get('PIC')
if baseDir == None:
  baseDir = '/tmp/MasterClass'
fullPath = os.path.join(baseDir,shotName)

try:
    os.makedirs(fullPath)
    nuke.message('Created dir %s' % fullPath)
except OSError:
    nuke.message('WARNING: err creating dir %s' % dir)
    pass

fileName = '%s.%s.%s' % (shotName, '%04d', ext)
fname = os.path.join(baseDir,shotName,fileName)

#### set the file knob to the new file name
nuke.thisNode()['file'].setValue(fname)
"""
	buttonKnob.setValue(script)

	#### add knobs to node
	for k in [tabKnob, jobKnob, shotKnob, versionKnob, takeKnob,labelKnob, buttonKnob, extKnob]:
	    node.addKnob(k)
	    
