# ###   Add Range Tab to selected nodes
# ###   Last modified: 08/31/2008
# ###   Written by Diogo Girondi
# ###   diogogirondi@gmail.com

import nuke
import nukescripts

def addrangetab():
    
    """Get the selected nodes in the DAG"""
    selnodes = nuke.selectedNodes()

    for i in selnodes:
        
        """Retrives node Class and the Root range"""
        _class = i.Class()
        _first = int(nuke.root().knob("first_frame").value())
        _last = int(nuke.root().knob("last_frame").value())
        
        """Set Knobs parameters"""
        rTab = nuke.Tab_Knob("rangetab", "Range")
        rIn = nuke.Int_Knob("range_in", "In")
        rOut = nuke.Int_Knob("range_out", "Out")
        rSetIn = nuke.Script_Knob("set_in", "Use Current", "knob this.range_in [frame]")
        rSetOut =nuke.Script_Knob("set_out", "Use Current", "knob this.range_out [frame]")
        rUse = nuke.Script_Knob("set_range", "Set Range", "in this.disable {set_expression {frame<this.range_in || frame>this.range_out}}")
        rTab = nuke.Tab_Knob("rangetab", "Range")
        
        """Adds Knobs to each node"""
        i.addKnob(rTab)
        i.addKnob(rIn)
        i.addKnob(rSetIn)
        i.addKnob(rOut)
        i.addKnob(rSetOut)
        i.addKnob(rUse)
        
        """Set default range values"""
        v = i['range_in']
        v.setValue(_first)
        v = i['range_out']
        v.setValue(_last)
        