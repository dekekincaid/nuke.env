def writeChecker():
    nuke.selectAll()
    allNodes = nuke.selectedNodes()
    
    writeNodes = {}
    
    for node in allNodes:
        if node.Class() == 'Write':
            key = node[ 'file' ].value().split( '/' )[-1]
            value =node
            writeNodes[ key ] = value
    
    nuke.invertSelection()    
    
    panel = nuke.Panel( 'Enable/Disable Write Nodes' )

    for key in sorted(writeNodes.keys()):
        disableCur = writeNodes[ key ][ 'disable' ].value()
        if disableCur == True:
            key = panel.addBooleanCheckBox( key, 'false' )
        else:
            key = panel.addBooleanCheckBox( key, 'true' )
    
    
    panel.addButton( "Disable\nAll" )
    panel.addButton( "OK" )
    panel.addButton( "Cancel" )
    panel.addButton( "Enabel\nAll" )
    
    action_result = panel.show()
    print action_result
    if action_result == 1:
        for key in writeNodes:
            if panel.value( key ) == 0:
                writeNodes[ key ][ 'disable' ].setValue( True )
            else:
                writeNodes[ key ][ 'disable' ].setValue( False )
    
    elif action_result == 3:
        for key in writeNodes:
            writeNodes[ key ][ 'disable' ].setValue( False )
    
    elif action_result == 0:
        for key in writeNodes:
            writeNodes[ key ][ 'disable' ].setValue( True )
    
    else:
        pass
