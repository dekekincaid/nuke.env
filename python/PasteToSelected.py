# PasteToSelected.py by Ean carr
# Sept 26, 08
#
# This pastes nodes in clipboard to each selected node. Based on Frank Rueter's
# PasteToSelected.tcl script which seems to be broken in 5.x.
#
# My version attempts to ignore Viewer and VIEWER_INPUT nodes, and leaves new nodes
# selected instead of original user selection.

import nuke, nukescripts

def PasteToSelected():

	# put selection in variable and find out if nodes are valid
	original_selection = nuke.selectedNodes()
	for node in original_selection:
		if node.Class() == "Viewer" or node.name() == "VIEWER_INPUT":
			node.knob("selected").setValue(False)
	valid_selection = nuke.selectedNodes()
	for a in nuke.allNodes():
		a.knob("selected").setValue(False)

	# create dict for new nodes so they can be selected later
	new_nodes = []

	# go through selection and paste from clipboard to each
	for b in valid_selection:
		b.knob("selected").setValue(True)
		nuke.nodePaste(nukescripts.cut_paste_file())
		new_nodes += nuke.selectedNodes()
		for pasted in nuke.selectedNodes():
			pasted.knob("selected").setValue(False)

	# re-select original nodes
	for c in new_nodes:
		c.knob("selected").setValue(True)

	if len(valid_selection) is not len(original_selection):
		nuke.message("Some Viewer or VIEWER_LUT nodes were ignored. Rad.")