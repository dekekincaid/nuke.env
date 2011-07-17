import nuke
def scaleNodes( scale ):
    nodes = nuke.selectedNodes()
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
        n.setXpos( centreX + ( n.xpos() - centreX ) * scale )
        n.setYpos( centreY + ( n.ypos() - centreY ) * scale )
