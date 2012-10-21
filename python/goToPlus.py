###    Go To Frame Plus
###    A more discreet* like 'go to frame'
###    ---------------------------------------------------------
###    goToPlus.py v1.0
###    Created: 23/04/2009
###    Modified: 23/04/2009
###    Written by Diogo Girondi
###    diogogirondi@gmail.com

import nuke
import re

def goToPlus():
    
    '''
    Allows you to directly enter simple math signs to
    go to a frame without explicity requiring you to
    enter the current frame number before it.
    '''
    
    cFrame = nuke.frame()
    
    p = nuke.Panel( 'Go to Frame Plus' )
    p.addSingleLineInput( '', '' )
    p.show()

    goTo = p.value( '' )
    pat1 = re.compile( '\+|-|\*|\/' )
    
    if goTo == '':
        return
    elif goTo[0].isdigit() == True and pat1.search( goTo ) == None:
        nuke.frame( int( goTo ) )
    elif goTo[0].isdigit() == True and pat1.search( goTo ) != None:
        try:
            nuke.frame( eval( goTo ) )
        except Exception, e:
            raise RuntimeError( e )
    else:
        try:
            nuke.frame( eval( str( int( cFrame ) ) + goTo ) )
        except Exception, e:
            raise RuntimeError( e )
            
            
            