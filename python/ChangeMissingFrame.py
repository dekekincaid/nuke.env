import nuke
def change_Missing():

	panel = nuke.Panel("Change Missing Frame Option")
	panel.addBooleanCheckBox("selectedNodes only", "0 1")
	panel.addEnumerationPulldown("missing frames", "error black checkerboard nearestframe")
	panel.show()
	m = panel.value("missing frames")
	n =panel.value("selectedNodes only")
	if n == True:
    		for i in nuke.selectedNodes():
        		i.knob("on_error").setValue(m)

	else: 
      		for a in nuke.allNodes("Read"):
           		a.knob("on_error").setValue(m)
