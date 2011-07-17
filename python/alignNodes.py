def alignNodes( nodes, direction = 'x' ):
    '''
    Align nodes either horizontally or vertically.
    '''
    if len( nodes ) < 2:
        return
    if direction.lower() not in ('x', 'y'):
        raise ValueError, 'direction argument must be x or y'

    positions = [ float( n[ direction.lower()+'pos' ].value() ) for n in nodes]
    avrg = sum( positions ) / len( positions )
    for n in nodes:
		if direction == 'x':
		    for n in nodes:
		        n.setXpos( int(avrg) )
		else:
		    for n in nodes:
		        n.setYpos( int(avrg) )

    return avrg