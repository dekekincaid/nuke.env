#!/usr/bin/env python

# ###  AssembleEdit v.20
# ###  Last modified: 01/25/2010
# ###  Written by Daniel Brylka
# ###  Please feel free to add/modify anything you want! The only thing I am asking is that should publish your work as well!
# ###  I am happy to hear about improvements and would like to incorporate them.
# ###  email:daniel@toodee.de

# ### A quick history of the script:
# ### I am working on autodesk flame for over 10 years on commercials and feature films. On my first Nuke job I had a client approved edit (this was nearly true)
# ### and no system available to me to assemble the edit in a form of DPX sequences. So I set up this script by hand and more than once miscalculated with the
# ### TimeOffsets (I set them up in the read node as 'frame-xxx'). This script is not supposed to be a conforming tool. But often I set up a job on flame, conform it and then
# ### pass out all the shots on a server for the 2D and 3D departments in a form of SH01 to SHxx...in this case I had a reference quicktime movie, I added frame numbers to it
# ### which makes it easy to count all the editpoints in the spot.

# ### Example: (1500 frames edit with 10 shots) in the file 'editpoints_1500.txt'
# ### sh01 1
# ### sh02 100
# ### sh03 237
# ### sh04 320
# ### sh05 545
# ### sh06 678
# ### sh07 889
# ### sh08 1011
# ### sh09 1250
# ### sh10 1425
# ### shxx 1500


def AssembleEdit():
    
    # Stuff that should come next:
    # 1. Nuke should delete all nodes if any are present in the script.
    # 2. A save node is missing;  I need to set the project length!

    import nuke
    import nukescripts
    
    # First I select all nodes in the script and delete them
    # nuke.allNodes()
    
    # nukescripts.node_delete()
    # Nuke is asking for some input
    # The actual editpoints.txt file
    # The path to the images - note! Right now the shot numbers can only have two letters and go up to 99 shots!
    # The format of the imagesequence - this could be read out of the files automatically!
    
    GetInfos = nuke.Panel("AssembleEdit_v20")
    GetInfos.addFilenameSearch("Editpoints-File: ", ".txt")
    GetInfos.addFilenameSearch("File paths for the Shots: ", "../01_images/")
    GetInfos.addSingleLineInput("Image-Type: ", "jpg")
    
    GetInfos.show()
    
    # print editpointsfilepath
    # print shotspath
    # print ImageType
    
    
    # Set up variables
    
    editpointsfilepath = GetInfos.value("Editpoints-File: ")
    ShotDir = GetInfos.value("File paths for the Shots: ")
    ImageType = GetInfos.value("Image-Type: ")
    
    assemble_edit = open(editpointsfilepath, 'r')
    
    shotnamelist = []
    shotframelist = []
    shotcounter = 0
    
    # fill the variale editlist with each line of the file and parse the first four characters
    # into the "shotnumber" and the frame numbers into "editpoint"
    
    for editlist in assemble_edit:
        # reads the shotnames and puts the stings into the list "shotnamelist"
        shotname = editlist[0:4]
        shotnamelist.append(shotname)
    
        # reads in the editpoints and add them to the list "shotlist"
        # the allowed max. framenumber would be 99.999 (5 digtits)
        editpoint = int(editlist[5:10])
        shotframelist.append(editpoint)
    
        # counts the number of shots in the edit
        shotcounter +=1
    
    # Print results for debuging    
    # print shotnamelist
    # print shotframelist
    # print
    # print 'shotcounter = ' +str(shotcounter)
    # print
    
    # Now I need to print out each shot in the list with its startframe and endframe.
    # The last edit is the end of the clip.
    # nthedit it the position in the list.
    # cut is the counter to work on each shot
    # The If/Else statement checks that I am not running out of my list.
    # Anyway, the last shot is not a new shot but the end of my edit.
    # The creation of Nuke nodes is also incorporated now.
    # The "nodecounter" is accessing the nodes numbers - it is important that the script is emtpy!
    
    # In the future I need to clean all nodes in Nuke before the script runs
    
    nthedit = 0
    nodecounter = 1
    readx = 'Read' + str(nodecounter)
    switchx = 'Switch' + str(nodecounter)
    timeoffx = 'TimeOffset' + str(nodecounter)
    
    for i in shotnamelist:
        print i
        if nthedit==0:
            
            # Create the first read node that is not running in the loop
            # no additional Nuke nodes are needed at this point
            rx = nuke.nodes.Read()
            seqxpath = ShotDir + i[0:4] + "/" + i + "_%04d." + ImageType
            
            # fill Read1 node with data
            nuke.toNode(readx).knob('file').setValue(seqxpath)
            nuke.toNode(readx).knob('first').setValue(1)
            nuke.toNode(readx).knob('last').setValue(shotframelist[nthedit+1]-1)
            
            # create a TimeOffset node with no offset - but just to have it match to the other node counters!
            slipx = nuke.nodes.TimeOffset(inputs=[rx])
            nuke.toNode(timeoffx).knob('time_offset').setValue(0)
            
            # create the first Switch node and connect it to the first read node! This is just a dummy switch with no function
            print 'what is timeoffx?'
            print timeoffx
            swix = nuke.nodes.Switch(inputs=[slipx, slipx])
            
            # creating keyframes for Switch1
            nuke.toNode(switchx).knob('which').setKeyAt(1)
            nuke.toNode(switchx).knob('which').setValueAt(0,1)
            # nuke.toNode(switchx).knob('which').setKeyAt(shotframelist[nthedit+1])
            # nuke.toNode(switchx).knob('which').setValueAt(1,shotframelist[nthedit+1])
            
            # print what I am working on...
            # print seqxpath
            # print i + ' starts at frame ' + str(shotframelist[nthedit]) + ' and ends at frame ' + str(shotframelist[nthedit+1])
            # print 'this is the first shot'
            
        elif nthedit<shotcounter-1:
            if nthedit == len(shotframelist)-2:
                
                # this checks if I approach the last edit. Here the last frame is actually the end frame of the whole sequence.
                # create the last read node - the last timeoffset and the last Switch node
                rx = nuke.nodes.Read()
                seqxpath = ShotDir + i[0:4] + "/" + i + "_%04d." + ImageType
                endframe = shotframelist[nthedit+1] - shotframelist[nthedit]
                
                # fill Readx nodes with data
                nuke.toNode(readx).knob('file').setValue(seqxpath)
                nuke.toNode(readx).knob('first').setValue(1)
                nuke.toNode(readx).knob('last').setValue(endframe)
                
                # create the last TimeOffset node
                slipx = nuke.nodes.TimeOffset(inputs=[rx])
                nuke.toNode(timeoffx).knob('time_offset').setValue(shotframelist[nthedit]-1)
                # print shotframelist[nthedit]
                # print timeoffx
                
                # create a Switch node and connect the two sequences
                swix = nuke.nodes.Switch()
                nuke.toNode(switchx).connectInput(0, swix_prev)
                nuke.toNode(switchx).connectInput(1, slipx)
                
                # creating keyframes for Switchx
                nuke.toNode(switchx).knob('which').setKeyAt(1)
                nuke.toNode(switchx).knob('which').setValueAt(0,1)
                nuke.toNode(switchx).knob('which').setKeyAt(shotframelist[nthedit])
                nuke.toNode(switchx).knob('which').setValueAt(1,shotframelist[nthedit])
                
                # print results
                # print seqxpath
                # print i + ' starts at frame ' + str(shotframelist[nthedit]) + ' and ends at frame ' + str(shotframelist[nthedit+1])
            else:
                
                # create the 2nd read node, the timeoffset and the switch nodes in a loop until to the end of the list
                rx = nuke.nodes.Read()
                seqxpath = ShotDir + i[0:4] + "/" + i + "_%04d." + ImageType
                endframe = shotframelist[nthedit+1] - shotframelist[nthedit]
                
                # fill Readx nodes with data
                nuke.toNode(readx).knob('file').setValue(seqxpath)
                nuke.toNode(readx).knob('first').setValue(1)
                nuke.toNode(readx).knob('last').setValue(endframe)
                
                # create a TimeOffset node
                slipx = nuke.nodes.TimeOffset(inputs=[rx])
                nuke.toNode(timeoffx).knob('time_offset').setValue(shotframelist[nthedit]-1)
                print shotframelist[nthedit]
                print timeoffx
                
                # create a Switch node and connect the two sequences
                swix = nuke.nodes.Switch()
                nuke.toNode(switchx).connectInput(0, swix_prev)
                nuke.toNode(switchx).connectInput(1, slipx)
                # creating keyframes for Switchx
                nuke.toNode(switchx).knob('which').setKeyAt(1)
                nuke.toNode(switchx).knob('which').setValueAt(0,1)
                nuke.toNode(switchx).knob('which').setKeyAt(shotframelist[nthedit])
                nuke.toNode(switchx).knob('which').setValueAt(1,shotframelist[nthedit])
                
                # print results
                # print seqxpath
                
                # otherwise each shot starts from it's edit point until the next editpoint -1
                # print i + ' starts at frame ' + str(shotframelist[nthedit]) + ' and ends at frame ' + str(shotframelist[nthedit+1]-1)
        else:
            
            # now the list is worked out and I can show my last frame of my last edit which is also the length of the whole edit!
            print 'Frame ' + str(shotframelist[nthedit]) + ' is the last frame.'
        # count up several varibles    
        nthedit +=1
        nodecounter += 1
        readx = 'Read' + str(nodecounter)
        timeoffx = 'TimeOffset' + str(nodecounter)
        switchx = 'Switch' + str(nodecounter)
        # "swix_prev" is now the previous created switch node 
        swix_prev = swix
    
       
    # print the summary of the editlist
    # fulledit has the number of edit which is the whole elements in the list -1
    
    fulledit = len(shotframelist)-1
    print
    print 'The edit has ' + str(fulledit) + ' shots and is ' + str(shotframelist[fulledit]) + ' frames long.'
    
    