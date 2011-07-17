###    Renames the selected nodes sequentially.
###    ---------------------------------------------------------
###    renameNodes.py v2.0
###    Created: 22/10/2009
###    Modified: 05/01/2010
###    Written by Diogo Girondi
###    diogogirondi@gmail.com

import re
import nuke

def renameNodes():
    
    '''Renames the selected nodes sequentially'''
    
    sn = nuke.selectedNodes()
    sn.reverse()
    if sn:
        newName = nuke.getInput( 'New name:' )
        if newName:
            if newName[0].isdigit():
                newName = '_' + newName
            if newName[-1].isdigit():
                newName += '_'
            pat = re.compile( '[\s\W]' )
            newName = pat.sub( '_', newName )
            
            for n in sn:
                n.setName( newName )