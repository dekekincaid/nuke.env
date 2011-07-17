import nuke
def holdFrames ( node, holdRange='all' ):
    """
    Append  frameHold node for each frame in range.
    if holdRange = 'all', the node's frame range is processed.
    if holdRange = valid frame range string, then range is processed
    if holdRange is not 'all', and not a valid frame range string, a panel is launched to get a valid range from the user.
    """
    if holdRange == 'all':
        fr = node.frameRange()
    else:
        try:     fr = nuke.FrameRange( holdRange )
        except:
                str = nuke.getFramesAndViews( 'Hold Frames', '%s-%sx1' % (node['first'].value(), node['last'].value()) )
                if not str:
                    return
                fr = nuke.FrameRange( str[0] )
            
        

    newNodes = []
    for f in xrange( fr.first(), fr.last()+1, +fr.increment() ):
        fh = nuke.nodes.FrameHold( first_frame=f, postage_stamp = True )
        fh.setInput( 0, node )
        newNodes.append( fh )
    node['postage_stamp'].setValue(False)
    return newNodes
