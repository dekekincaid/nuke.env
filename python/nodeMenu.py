#too much stuff burried in edit>node
#recreated as a top bar menu item
#taken from menu.py in the nuke install and copied it here
#6.2v4
##########################################################################################
import sys
import os.path
import nuke


menuNk=nuke.menu("Nuke")
n=menuNk.addMenu("Node")
isLinux = not nuke.env['WIN32'] and not nuke.env['MACOS']

n.addCommand("&Filename/Show", "nukescripts.showname()", "q")
#n.addCommand("&Filename/Search and Replace...", "nukescripts.search_replace()", "^+?" if isLinux else "^+/")
n.addCommand("&Filename/Set Versions", "nuke.tcl('cam_ver_panel')")
n.addCommand("&Filename/Version Up", "nukescripts.version_up()", "#Up")
n.addCommand("&Filename/Version Down", "nukescripts.version_down()", "#Down")
n.addCommand("&Filename/Version to Latest (Reads only)", "nukescripts.version_latest()", "#+Up")
n.addCommand("&Filename/Camera Up", "nukescripts.camera_up()", "#Right")
n.addCommand("&Filename/Camera Down", "nukescripts.camera_down()", "#Left")

n.addCommand("&Group/&Collapse To Group", "nuke.collapseToGroup()", "^g")
n.addCommand("&Group/&Expand Group", "nuke.expandSelectedGroup()", "^#g")
# Add another one hidden to get Ctrl+Enter (keypad) as well as Ctrl+Return
n.addCommand("&Group/&Open Group Node Graph", "nuke.showDag(nuke.selectedNode())", "^Enter")
n.addCommand("@;&Open Group Node Graph", "nuke.showDag(nuke.selectedNode())", "^Return")
n.addCommand("&Group/Copy &Nodes To Group", "nuke.makeGroup()", "^#+g")
n.addCommand("&Group/Copy Gi&zmo To Group", "nuke.tcl('copy_gizmo_to_group [ selected_node ]')", "^+g")

n.addCommand("&Color...", "nukescripts.color_nodes()", "^+c")
n.addCommand("&Un-color", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
	i.knob(\"tile_color\").setValue(0)\n\
")
n.addCommand("Paste Knob &Values", "nukescripts.copy_knobs(\"\")", "^#V")
n.addCommand("&Input On\/Off", "nukescripts.toggle(\"hide_input\")", "#h")
n.addCommand("&Postage Stamp On\/Off", "nukescripts.toggle(\"postage_stamp\")", "#p")
n.addCommand("Force &Dope Sheet On\/Off", "nukescripts.toggle(\"dope_sheet\")", "#d")

#def _autoplace():
#  n = nuke.selectedNodes()
#  for i in n:
#    nuke.autoplace(i)

#n.addCommand("Auto&place", "_autoplace()", "l")
#n.addCommand("&Buffer On\/Off", "nukescripts.toggle(\"cached\")", "^b")
#n.addCommand("&Disable\/Enable", "nukescripts.toggle(\"disable\")", "d")
n.addCommand("&Info Viewer", "nukescripts.infoviewer()", "i")
n.addCommand("&Open Selected", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  nuke.show(i)\n\
", "0xff0d")
n.addCommand("&Snap to Grid", "\n\
n = nuke.selectedNodes()\n\
for i in n:\n\
  nuke.autoplaceSnap(i)\n\
", "|")
n.addCommand("&Snap All to Grid", "\n\
n = nuke.allNodes();\n\
for i in n:\n\
  nuke.autoplaceSnap(i)\n\
", "\\",)
n.addCommand("Swap A - B", "nukescripts.swapAB(nuke.selectedNode())", "+X")
n.addCommand("Connect", "nuke.connectNodes(False, False)", "y")
n.addCommand("Connect Backward", "nuke.connectNodes(True, False)", "+y")
n.addCommand("Connect A", "nuke.connectNodes(False, True)", "#y")
n.addCommand("Connect Backward - A", "nuke.connectNodes(True, True)", "+#y")
n.addCommand("Splay First", "nuke.splayNodes(False, False)", "u")
n.addCommand("Splay Last", "nuke.splayNodes(True, False)", "+u")
n.addCommand("Splay First to A", "nuke.splayNodes(False, True)", "#u")
n.addCommand("Splay Last to A", "nuke.splayNodes(True, True)", "+#u")

def _copyKnobsFromScriptToScript(n, m):
  k1 = n.knobs()
  k2 = m.knobs()
  excludedKnobs = ["name", "xpos", "ypos"]
  intersection = dict([(item, k1[item]) for item in k1.keys() if item not in excludedKnobs and k2.has_key(item)])
  for k in intersection.keys():
    x1 = n[k]
    x2 = m[k]
    x2.fromScript(x1.toScript(False))

def _useAsInputProcess():
  n = nuke.selectedNode()
  [i['selected'].setValue(False) for i in nuke.allNodes()]
  # FIXME: these two calls should have the arguments in the same order, or even better change the node bindings so they can go.
  if nuke.dependencies([n], nuke.INPUTS | nuke.HIDDEN_INPUTS) or nuke.dependentNodes(nuke.INPUTS | nuke.HIDDEN_INPUTS, [n]):
    m = nuke.createNode(n.Class())
  else:
    m = n
  if m is not n: _copyKnobsFromScriptToScript(n, m)
  viewer = nuke.activeViewer().node()
  viewer['input_process'].setValue(True)
  viewer['input_process_node'].setValue(m.name())

def _copyViewerProcessToDAG():
  vpNode = nuke.ViewerProcess.node()
  [i['selected'].setValue(False) for i in nuke.allNodes()]
  n = nuke.createNode(vpNode.Class())
  _copyKnobsFromScriptToScript(vpNode, n)

n.addCommand("Use as Input Process", "_useAsInputProcess()")
n.addCommand("Copy Viewer Process to Node Graph", "_copyViewerProcessToDAG()")