###   Sequencer for Nuke
###   It will add a entry for every for every selected Write node to the .bat file
###   v1.1 - Last modified: 10/13/2008
###   Written by Diogo Girondi
###   diogogirondi@gmail.com

import nuke

def sequencer(mode=0):
    
    """
    Sequencer will cut/offset every selected node based on the selection order
    
    Passing no arguments it assumes the default and runs in "TimeOffset" mode
    
        0 -> for TimeOffset mode
        1 -> for Retime mode
    
    """
    
    sn = nuke.selectedNodes()
    sn.reverse()

    sequencer = []

    def _with_timoffset(sel):
        
        for n in sel:
            for i in sel:
                n.knob('selected').setValue(False)
            n.knob('selected').setValue(True)
            rt = nuke.createNode('TimeOffset', '', False)
            rt.knob('selected').setValue(False)
            sequencer.append(rt)
            
        for rt in sequencer:
            idx = sequencer.index(rt)
            
            if idx == 0:
                idx = idx
                rt.knob('label').setValue("Cut " + str(idx+1))
                continue
            else:
                idx = idx-1
                offset = float(nuke.value(sequencer[idx].name()+".last_frame"))+1.0
                rt.knob('selected').setValue(True)
                rt.knob('time_offset').setValue(offset)
                rt.knob('label').setValue("Cut " + str(idx+2))
                rt.knob('selected').setValue(False)
                continue
                
                
                
    def _with_retime(sel):
        
        for n in sel:
            for i in sel:
                i.knob('selected').setValue(False)
            n.knob('selected').setValue(True)
            
            start = float(nuke.value(n.name()+".first_frame"))
            end = float(nuke.value(n.name()+".last_frame"))
            
            rt = nuke.createNode('Retime', '', False)
            
            rt.knob('input.first_lock').setValue(True)
            rt.knob('input.last_lock').setValue(True)
            rt.knob('output.first_lock').setValue(True)
            rt.knob('output.last_lock').setValue(True)
            rt.knob('input.first').setValue(start)
            rt.knob('input.last').setValue(end)
            rt.knob('output.first').setValue(start)
            rt.knob('output.last').setValue(end)
            rt.knob('before').setValue('black')
            rt.knob('after').setValue('black')
            rt.knob('selected').setValue(False)
            
            sequencer.append(rt)
            
        for rt in sequencer:
            idx = sequencer.index(rt)
            
            if idx == 0:
                idx = idx
                rt.knob('label').setValue("Cut " + str(idx+1))
                continue
            else:
                idx = idx-1
                newStart = sequencer[idx].knob('output.last').value() + 1
                newEnd = rt.knob('output.last').value() + sequencer[idx].knob('output.last').value()
                rt.knob('selected').setValue(True)
                rt.knob('output.first').setValue(newStart)
                rt.knob('output.last').setValue(newEnd)
                rt.knob('label').setValue("Cut " + str(idx+2))
                rt.knob('selected').setValue(False)
                continue 
                
                
                
    if len(sn) < 2:
        nuke.message("Select at least 2 nodes in the\norder you want your 'cuts' to happen")
    else:
        if mode == 0:
            _with_timoffset(sn)
        elif mode == 1:
            _with_retime(sn)
        else:
            nuke.message("Valid arguments\n0: Use TimeOffset nodes\n1: Use Retime nodes")
            
            
            