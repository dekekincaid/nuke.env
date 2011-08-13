import nuke


def thumbnailer():
    selNodes = []
    selNodes = nuke.selectedNodes('Read')
    if not selNodes:
        selNodes = nuke.allNodes('Read')
        
    for readNode in selNodes:
        readNode.knob('postage_stamp').setValue(False)
        
        depNodes = readNode.dependent()
        
        isThumbnailed = False
        
        for node in depNodes:
            if node.Class() == 'FrameHold' and node.knob('name').value() == '%s_stamp' % ( readNode.name() ):
                node.knob('first_frame').setValue( nuke.frame() )
                isThumbnailed = True
        
        if not isThumbnailed:
            nameMask = '%s_stamp' % ( readNode.name() )
            thumbnailer = nuke.nodes.FrameHold( name = nameMask, postage_stamp = True, first_frame = nuke.frame(), tile_color = 4294967295)
            thumbnailer.setInput( 0, readNode )
            thumbnailer.setXYpos( readNode.xpos(), readNode.ypos()-80 )