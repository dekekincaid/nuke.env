import nuke

def scaleNodes( xScale, yScale=None ):
    def getSideNodes( bd ):
        '''return a given backdrop node's "side nodes" (left, right, top andbottom most nodes) as a dictionary including the nodes and the respective DAG coordinates'''
        origSel = nuke.selectedNodes()
        [ n.setSelected( False ) for n in origSel ]
        
        bd.selectNodes()
        bdNodes = nuke.selectedNodes()
        [ n.setSelected( False ) for n in bdNodes ]  #DESELECT BACKDROP NODES
        [ n.setSelected( True ) for n in origSel ]  #RESTORE ORIGINAL SELECTION  
        if not bdNodes:
            return []
        
        leftNode = rightNode = bottomNode = topNode= bdNodes[0] # START WITH RANDOM NODE
        for n in bdNodes:
            if n.xpos() < leftNode.xpos():
                leftNode = n
            if n.xpos() > rightNode.xpos():
                rightNode = n
            if n.ypos() < topNode.ypos():
                topNode = n
            if n.ypos() > bottomNode.ypos():
                bottomNode = n

        return dict( left=[leftNode, nuke.math.Vector2( leftNode.xpos(), leftNode.ypos()) ], right=[rightNode, nuke.math.Vector2( rightNode.xpos(), rightNode.ypos()) ], top=[topNode, nuke.math.Vector2( topNode.xpos(), topNode.ypos()) ], bottom=[bottomNode, nuke.math.Vector2( bottomNode.xpos(), bottomNode.ypos()) ])

   # MAKE THINGS BACKWARDS COMPATIBLE
    yScale = yScale or xScale

   # COLLECT SIDE NODES AND COORDINATES FOR BACKDROPS
    backdrops = {}
    for bd in nuke.allNodes( 'BackdropNode' ):
        backdrops[bd] = getSideNodes( bd )

    # MOVE NODES FROM CENTRE OUTWARD
    nodes = [ n for n in nuke.selectedNodes() if n.Class() != 'BackdropNode' ]
    amount = len( nodes )
    if amount == 0:    return

    allX = 0
    allY = 0
    for n in nodes:
        allX += n.xpos()
        allY += n.ypos()

    centreX = allX / amount
    centreY = allY / amount

    for n in nodes:
        n.setXpos( int( centreX + ( n.xpos() - centreX ) * xScale ) )
        n.setYpos( int( centreY + ( n.ypos() - centreY ) * yScale ) )

    #ADJUST BACKDROP NODES
    for bd,bdSides in backdrops.iteritems():
        leftDelta = bdSides['left'][0].xpos() - bdSides['left'][1].x
        topDelta = bdSides['top'][0].ypos() - bdSides['top'][1].y
        rightDelta = bdSides['right'][0].xpos() - bdSides['right'][1].x
        bottomDelta = bdSides['bottom'][0].ypos() - bdSides['bottom'][1].y


        bd.setXpos( int( bd.xpos() + leftDelta ) )
        bd.setYpos( int( bd.ypos() + topDelta ) )

        bd['bdwidth'].setValue( int( bd['bdwidth'].value() - leftDelta + rightDelta ) )
        bd['bdheight'].setValue( int( bd['bdheight'].value() - topDelta + bottomDelta ) )
