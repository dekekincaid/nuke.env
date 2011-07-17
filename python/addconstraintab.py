# ###   Adds a Look Tab where you can set a camera to always look at a object
# ###   Derived from a TCL original by Frank Rueter and Broesler
# ###   Thanks to Jack Binks for all the help and patience ;)
# ###   v1.0 - Last modified: 09/02/2008
# ###   Written by Diogo Girondi
# ###   diogogirondi@gmail.com

import nuke
import nukescripts

def constrain():
    
    """Get the selected nodes in the DAG"""
    selNodes = nuke.selectedNodes()
    
    """ Classes that will allow this script to run """
    listNodes = ['Cube', 'Sphere', 'Axis2', 'Card2', 'Cylinder', 'ReadGeo2', 'Spotlight', 'Light2', 'DirectLight', 'Camera', 'Camera2', 'Card']
    cleanList = set(listNodes)
    
    """ Run for each selected node """
    for i in selNodes:
        
        """ Get the Class for each node """
        _class = i.Class()
        
        """ If Class is found on the list (listNodes) add the knobs, otherwise delete vars and do nothing """
        if _class in cleanList:
            
            """ Sets Knobs """
            lookTab = nuke.Tab_Knob("look", "Constrain")
            target = nuke.EvalString_Knob("look_at", "Look at")
            setlookObject = nuke.PyScript_Knob("set", "Set", "selNodes = nuke.selectedNodes()\n\nif len(selNodes) == 1:\n\tthisNode = selNodes[-1]\n\tk = thisNode['look_at']\n\t\n\tif k.value() == \"\":\n\t\tlookAt = nuke.getInput(\'Type the target node name\')\n\t\tk.setValue(lookAt)\n\n\telse:\n\t\tlookAt = k.value()\n\t\tk.setValue(lookAt)\n\nelif len(selNodes) > 1:\n\tthisNode = selNodes[-1]\n\tlookAt = selNodes[-2]\n\tk = thisNode['look_at']\n\tk.setValue(lookAt.name())\n\t\nelse:\n\tpass\n\nlookObject = k.value()\n\nxX = \'degrees(atan2(\' + lookObject + \'.translate.y-translate.y,sqrt(pow(\' + lookObject + \'.translate.x-translate.x,2)+pow(\' + lookObject + \'.translate.z-translate.z,2))))\'\nyX = lookObject + \'.translate.z-this.translate.z >= 0 ? 180+degrees(atan2(\' + lookObject + \'.translate.x-translate.x,\' + lookObject + \'.translate.z-translate.z)):180+degrees(atan2(\' + lookObject + \'.translate.x-translate.x,\' + lookObject + \'.translate.z-translate.z))\'\n\nthisNode['rotate'].setExpression(xX, 0)\nthisNode['rotate'].setExpression(yX, 1)\n")
            
            """ Adds Knobs """
            i.addKnob(lookTab)
            i.addKnob(target)
            i.addKnob(setlookObject)
            
        else:
            pass
    
    
    
    