# showmetadata.py 
# Author: Antony Nasce, The Foundry
# About: This script displays a MetaData Modal dialog of the selected node
# Usage: Add this code to you menu.py, select a node then press Alt+M to bring up the MetaData window.

import nuke

# Show MetaData Window
def showMeta():
  metakeys = nuke.thisNode().metadata().keys()
  metavalues = nuke.thisNode().metadata().values()
  metaData = ''
  numKeys = len(metakeys)
  for i in range(numKeys):
    metaData = metaData + metakeys[i] + ': ' + str(metavalues[i]) + '\n'
  return metaData
    
# Node Actions menu
menubar=nuke.menu("Node Graph")
m = menubar.addMenu("MetaData")
m.addCommand("Show MetaData","nuke.display('showMeta()', nuke.selectedNode(),'MetaData at ' + nuke.selectedNode().name())","#m")