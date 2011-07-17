###   Adds a Reader from selected Write node(s)
###   v3.0 - Last modified: 09/30/2008
###   Written by Diogo Girondi
###   diogogirondi@gmail.com

import os
import stat
import nuke
from time import strftime

def readwrites(blankread=False, check=True, threshold=100000, report=True):
    
    """
    Spawns a Read node(s) from selected Write node(s) and check it's files.
    
    readwrites(arg1, arg2, arg3)
    
    arg1: True: Spawn blank read with empty selections or write nodes
             False: Don't spawn anything for empty selections or write nodes
            
    arg2: True or False, Check for suspicious file sizes in the source folder.
    
    arg3: Integer, set's the threshold for bad files in bytes
    
    arg4: True or False, prints a report of the suspecious files to the terminal
    
    """
    
    def _checkbadframes(node, report):
        
        file = node.knob('file').value()
        folder = file.rstrip(file.split('/').pop())
        
        suspects = {}
            
        for f in os.listdir(folder):
            if os.path.isfile(folder + f):
                file_size = os.stat(folder + f).st_size
                if file_size < threshold:
                    suspects[f] = int(file_size)
                    
        if suspects != {}:
            node.knob('tile_color').setValue(-1308622593)
            
            if report == True:
                
                ordered_suspects = sorted(suspects.items(), key=lambda (k,v): (k,v))
                tprintlist = []
                spacing = 14
                GB = 1073741824.0
                MB = 1048576.0
                KB = 1024.0
                
                for each in ordered_suspects:
                    
                    if each[1] < KB:
                        size = "%d" % each[1] + " bytes"
                    elif each[1] < MB:
                        size = "%0.1f" % (float(each[1] / KB)) + " KB"
                    elif each[1] < GB:
                        size = "%0.2f" % (float(each[1] / MB)) + " MB"
                    elif each[1] >= GB:
                        size = "%0.0f" % (float(each[1] / GB)) + " GB"
                        
                    tprintlist.append("- " + each[0] + "  " + size)
                
                for each in tprintlist:
                    if len(each) > spacing:
                        spacing = len(each)
                
                div = "=" * spacing
                header = "__File" + "_" * (spacing - 13) + "Size___"
                
                nuke.tprint("")
                nuke.tprint(div)
                nuke.tprint(strftime("%H:%M:%S") + " Bad frames for: " + node.name())
                nuke.tprint(div)
                nuke.tprint(header)
                for each in tprintlist:
                    nuke.tprint(each)
                nuke.tprint(div)
                
            else:
                pass
                
        return None
    
    
    def _readwrites(blankread, check, threshold,  report):
        
        sn = [n for n in nuke.selectedNodes() if n.Class() == "Write"]
        
        if sn == [] and blankread == True:
            nuke.createNode("Read", "", True)
            
        elif sn == [] and blankread == False:
            return None
            
        elif sn != []:
            for n in sn:
                
                file = n.knob('file').value()
                proxy = n.knob('proxy').value()
                colorspace = n.knob('colorspace').value()
                premult = n.knob('premultiplied').value()
                rawdata = n.knob('raw').value()
                xpos = n.knob('xpos').value()
                ypos = n.knob('ypos').value()
                
                firstFrame = nuke.value(n.name()+".first_frame")
                lastFrame = nuke.value(n.name()+".last_frame")
                
                if file == '' and proxy == '':
                    if blankread == True:
                        read = nuke.createNode("Read", "", False)
                        read.knob('xpos').setValue(xpos)
                        read.knob('ypos').setValue(ypos + 80)
                        nuke.inputs(read, 0)
                        continue
                    elif blankread == False:
                        continue
                
                args = 'file {%s} proxy {%s} first %s last %s colorspace %s premultiplied %s raw %s' % (file, proxy, firstFrame, lastFrame, colorspace, premult, rawdata)
                
                read = nuke.createNode('Read', args)
                read.knob('xpos').setValue(xpos)
                read.knob('ypos').setValue(ypos + 80)
                nuke.inputs(read, 0)
                if check == True:
                    _checkbadframes(read, report)
                    continue
                    
                else:
                    continue
                    
                return None
                
        else:
            return None 
        
    
    _readwrites(blankread, check, threshold, report)
    
    