import nuke
import nukescripts

def convertGizmosToGroups():
   ###Node Selections
   nodeSelection = nuke.selectedNodes()
   noGizmoSelection = []
   gizmoSelection = []
   for n in nodeSelection:
       if 'gizmo_file' in n.knobs():
           gizmoSelection.append(n)
       else:
           noGizmoSelection.append(n)
   groupSelection = []

   for n in gizmoSelection:
       bypassGroup = False
       ###Current Status Variables
       nodeName = n.knob('name').value()
       nodeXPosition = n['xpos'].value()
       nodeYPosition = n['ypos'].value()
       nodeHideInput = n.knob('hide_input').value()
       nodeCached = n.knob('cached').value()
       nodePostageStamp = n.knob('postage_stamp').value()
       nodeDisable = n.knob('disable').value()
       nodeDopeSheet = n.knob('dope_sheet').value()
       nodeDependencies = n.dependencies()
       nodeMaxInputs = n.maxInputs()
       inputsList = []

       ###Current Node Isolate Selection
       for i in nodeSelection:
           i.knob('selected').setValue(False)            
       n.knob('selected').setValue(True)

       nuke.tcl('copy_gizmo_to_group [selected_node]')

       ###Refresh selections
       groupSelection.append(nuke.selectedNode())
       newGroup = nuke.selectedNode()

       ###Paste Attributes
       newGroup.knob('xpos').setValue(nodeXPosition)
       newGroup.knob('ypos').setValue(nodeYPosition)
       newGroup.knob('hide_input').setValue(nodeHideInput)
       newGroup.knob('cached').setValue(nodeCached)
       newGroup.knob('postage_stamp').setValue(nodePostageStamp)
       newGroup.knob('disable').setValue(nodeDisable)
       newGroup.knob('dope_sheet').setValue(nodeDopeSheet)

       ###Connect Inputs
       for f in range(0, nodeMaxInputs):
           inputsList.append(n.input(f))
       for num, r in enumerate(inputsList):
           newGroup.setInput(num, None)
       for num, s in enumerate(inputsList):
           newGroup.setInput(num, s)

       n.knob('name').setValue('temp__'+nodeName+'__temp')
       newGroup.knob('name').setValue(nodeName)

       newGroup.knob('selected').setValue(False)

   ###Cleanup (remove gizmos, leave groups)
   for y in gizmoSelection:
       y.knob('selected').setValue(True)
   nukescripts.node_delete(popupOnError=False)
   for z in groupSelection:
       z.knob('selected').setValue(True)
   for w in noGizmoSelection:
       w.knob('selected').setValue(True)