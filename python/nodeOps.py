# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# 
# Example that toggles viewer pipes off and on
#

import nuke

def toggleViewerPipes ():
   for n in nuke.allNodes('Viewer'):
       curValue = n['hide_input'].value()
       n['hide_input'].setValue(not curValue)
