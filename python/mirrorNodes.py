def mirrorNodes( nodes, direction = 'x' ):
    '''
    Mirror nodes either horizontally or vertically.
    '''
    if len( nodes ) < 2:
        return
    if direction.lower() not in ('x', 'y'):
        raise ValueError, 'direction argument must be x or y'

    if direction.lower() == 'x':
        positions = [ float( n.xpos()+n.screenWidth()/2 ) for n in nodes ]
    else:
        positions = [ float( n.ypos()+n.screenHeight()/2 ) for n in nodes ]

    axis = sum( positions ) / len( positions )
    for n in nodes:
        if direction.lower() == 'x':
            n.setXpos( int( n.xpos() - 2*(n.xpos()+n.screenWidth()/2-axis) ) )
        else:
            n.setYpos( int( n.ypos() - 2*(n.ypos()+n.screenHeight()/2-axis) ) )

    return axis
