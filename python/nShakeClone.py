#  nShakeClone.py
#  Nuke Python Module
#
#  Recreates a shake style "uni-directional" clone
#
#  Created by Jesse Spielman on 8/26/2010
#  jesse@themolecule.net
#
#	version 1.0 on 8/26/2010
#	Initial release
#
#	version 1.1 on 10/25/2010
#	bugfix suggested by Hugh Macdonald to work around cloning array_knobs using setSingleValue()
#
#	version 1.2 on 3/10/2011
#	improvement suggested by Michael Habenicht to handle String Knobs
#
#       version 1.3 on 3/10/2012
#       Added comments / removed some debug statements
#
#  Take all selected nodes and create dupliates that are linked via expressions 
#  to the original for all knobs except those an EXCLUSION_LIST...there may be 
#  value in defining different EXCLUSION_LISTs per node class...
#
#  Copyright 2010 The Molecule.
#  http://www.themolecule.net
#  All rights reserved.
#
#  Software is provided "as is," which means no guarantees!
import nuke

def shakeClone():
	EXCLUSION_LIST = ["xpos","ypos","help","hide_input","note_font_color","onCreate","updateUI","knobChanged","note_font","tile_color","selected","autolabel","process_mask","label","onDestroy","inject","indicators","maskFrom","maskChannelMask","maskChannelInput","Mask","postage_stamp","disable","maskChannelMask", "panel", "maskFromFlag","name","cached","fringe", "maskChannelInput" , "note_font_size" , "filter", "gl_color","transform"]

	originals = nuke.selectedNodes()
	[ n['selected'].setValue(False) for n in nuke.allNodes() ]
	
	for original in originals:
		new = nuke.createNode(original.Class())
		
		for i in original.knobs():
			if i not in EXCLUSION_LIST:
                                # Try to set the expression on the knob
				new.knob(i).setExpression("%s.%s" % (original.name(), original.knob(i).name()))
                                
                                # This will fail if the knob is an Array Knob...use setSingleValue to compensate
                                # Thanks Hugh!
				if isinstance(new.knob(i), nuke.Array_Knob):
					new.knob(i).setSingleValue(original.knob(i).singleValue()) 

                                # This will fail if the knob is a String Knob...use a TCL expression link to compensate
                                # Thanks Michael!
				elif isinstance(new.knob(i), nuke.String_Knob): 
					new.knob(i).setValue("[value %s.%s]" % (original.name(), original.knob(i).name())) 
					
		new['selected'].setValue(False)	

	[ n['selected'].setValue(True) for n in originals ]
			

# Add a menu / keyboard shortcut for this command
#menu = nuke.menu('Nuke')
#molTools = menu.addMenu('Molecule Tools')
#molTools.addCommand( 'Shake Style Clone', 'shakeClone()', "Alt+v")
