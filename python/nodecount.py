# ###   Nodecount with silly custom messages
# ###   Copyright (c) 2008 Twister Studio
# ###   Last modified: 04/12/2008
# ###   Written by Diogo Girondi
# ###   diogogirondi@gmail.com

import nuke
import nukescripts
from random import randint

def nodecount():
    
    an = len(nuke.allNodes())
    sn = len(nuke.selectedNodes())

    if sn == 1: tns = "node"
    else: tns = "nodes"
        
    if an <= 100: tx = "Ok, you're just starting."
    elif an <= 300: tx = "Keep going..."
    elif an <= 500: tx = "Keep this damn thing clean!"
    elif an <= 700: tx = "Are you lost, yet?"
    elif an <= 1000: tx = "Are you sure of that?"
    else: tx = "Good luck on rendering this fat baby."

    nuke.message(tx + "\n Total nodes: " + str(an) + "\n Selected " + tns + ": " +str(sn))