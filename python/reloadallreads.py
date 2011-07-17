###   Reloads all Read nodes present in a DAG
###   v1.0 - Last modified: 09/29/2008
###   Written by Diogo Girondi
###   diogogirondi@gmail.com

import nuke

def reloadallreads():
    
    an = [n for n in nuke.allNodes() if n.Class() == "Read"]
    
    if an != []:
        for n in an:
            n.knob('reload').execute()
    else:
        pass 