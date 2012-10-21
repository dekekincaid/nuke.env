### replaceChecker.py v1.0 20/05/2010, Ant Nasce, The Foundry Visionmongers Ltd.
## README
#This is a script aimed at debugging for Support queries.
#This script replaces all Read nodes and replaces them with Static checkerboards of the same format
#This script can handle replacement of Read nodes Groups and in the DAG.
#
# Usage: In your Nuke session, (with the script you wish to modify), execute readToChecker()
#
## Still to do:
# 1) Deal with Groups within Groups, within Groups...
# 2) Deal with Gizmos
# 3) Batch script conversion

from __future__ import with_statement      

# ReplaceWithFormat Method
def replaceWithFormat(thisNode, withNode):
    print 'Replacing '+ thisNode.name() + ' with Checkerboard...'
    oldNode = thisNode
    oldNodeX = oldNode.xpos()
    oldNodeY = oldNode.ypos()
    oldNodeFormat = oldNode.knob('format').value()
    oldNodeConnections = oldNode.dependent(nuke.INPUTS)
    
    # Delete the Read node
    nuke.delete(oldNode)
    newNode = nuke.createNode(withNode)
    for n in oldNodeConnections:
      n.setInput(0,newNode)

    # Set the original XYPos of the Node
    newNode.setXYpos(oldNodeX,oldNodeY)
    
    # set the format
    newNode.knob('format').setValue(oldNodeFormat)
    print 'Done'

# Method to call for doing the conversion of Reads to Checkerboard
def readToChecker():
    # Render out all Read nodes with Zipline EXRs
     for n in nuke.allNodes():
       if n.Class() == 'Read':
         replaceWithFormat(n,'CheckerBoard2')
       
       # Go inside Groups nodes and do the same... 
       elif n.Class()=='Group':
            with nuke.toNode(n.name()) as myGroup:
              for k in myGroup.nodes():
                if k.Class()=='Read': 
                  replaceWithFormat(k,'CheckerBoard2')