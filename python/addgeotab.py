# ###   Add GEO Tab to the selected Bezier node
# ###   Derived from a TCL original by frank@beingfrank.info
# ###   Requires Frank's "BezierGeoProc.tcl" installed in Nuke's path
# ###   Last modified: 08/31/2008
# ###   Written by Diogo Girondi
# ###   diogogirondi@gmail.com

import nuke
import nukescripts

def addgeotab():

    """Get the selected nodes in the DAG"""
    selnodes = nuke.selectedNodes()
    
    """ Run for each selected node """
    for i in selnodes:
        
        """Retrives node Class"""
        _class = i.Class()
        
        """Check node Class and add tab and knobs if successful"""
        if _class == "Bezier":
            geoTab = nuke.Tab_Knob("geotab", "Geo")
            gList = nuke.Enumeration_Knob("shapelist", "Shape", ["circle", "square", "oval", "rectangle", "triangle"])
            gSet = nuke.Script_Knob("set_geo", "Set Shape", "BezierGeoProc [knob this.shapelist]")
            
            i.addKnob(geoTab)
            i.addKnob(gList)
            i.addKnob(gSet)
            
        else:
            """If no Bezier is found, do nothing"""
            pass
