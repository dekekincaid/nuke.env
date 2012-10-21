## this script was assembled by j.hezer for studiorakete 2012 all input comes from frank rueter, ivan busquet and Michael Garrett 
## still wip with worldToNDC and worldToCamera only

import nuke
import os
import math
    
def getMetadataMatrix(meta_list):
    m = nuke.math.Matrix4()
    try:
        for i in range (0,16) :
            m[i] = meta_list[i]   
    except:
        m.makeIdentity()
    return m    

def ExrToCamera():
    try:
        selectedNode = nuke.selectedNode()
        nodeName = selectedNode.name()
        node = nuke.toNode(nodeName)
        if nuke.getNodeClassName(node) != 'Read':
            nuke.message('Please select a read Node')
            print 'Please select a read Node'
            return
        metaData = node.metadata()
        reqFields = ['exr/%s' % i for i in ('worldToCamera', 'worldToNDC')]
        if not set( reqFields ).issubset( metaData ):
            nuke.message('no basic matrices for camera found')
            print 'no basic matrices for camera found'
            return
        else:
            print 'found needed data'
        imageWidth = metaData['input/width']
        imageHeight = metaData['input/height']
        aspectRatio = float(imageWidth)/float(imageHeight)
        hAperture = 36.0
        vAperture = hAperture/aspectRatio
        
        # get additional stuff
        first = node.firstFrame()
        last = node.lastFrame()
        ret = nuke.getFramesAndViews( 'Create Camera from Metadata', '%s-%s' %( first, last )  )
        frameRange = nuke.FrameRange( ret[0] )
        camViews = (ret[1])
        
        
        for act in camViews:
            cam = nuke.nodes.Camera (name="Camera %s" % act)
            #enable animated parameters
            cam['useMatrix'].setValue( True )
            cam['haperture'].setValue ( hAperture )
            cam['vaperture'].setValue ( vAperture )
        
            for k in ( 'focal', 'matrix', 'win_translate'):
                cam[k].setAnimated()
            
            task = nuke.ProgressTask( 'Baking camera from meta data in %s' % node.name() )
    
            for curTask, frame in enumerate( frameRange ):
                if task.isCancelled():
                    break
                task.setMessage( 'processing frame %s' % frame )
            #get the data out of the exr header
                wTC = node.metadata('exr/worldToCamera',frame, act)
                wTN = node.metadata('exr/worldToNDC',frame, act)
                
            #set the lenshiift if additional metadata is available or manage to calculate it from the toNDC matrix    
                #cam['win_translate'].setValue( lensShift, 0 , frame )
                
            # get the focal length out of the worldToNDC Matrix
            # thats the wip part any ideas ??
                
                worldNDC = wTN
                
                lx =  (-1 - worldNDC[12] - worldNDC[8]) / worldNDC[0]
                rx =  (1 - worldNDC[12] - worldNDC[8]) / worldNDC[0]
                by = (-1 - worldNDC[13] - worldNDC[9]) / worldNDC[5]
                ty = (1 - worldNDC[13] - worldNDC[9]) / worldNDC[5]
                swW = max( lx , rx ) - min( lx , rx )  # Screen Window Width
                swH = max( by , ty ) - min( by , ty )  # Screen Window Height
                focal = hAperture / swW
                cam['focal'].setValueAt(  float( focal ), frame )
            
            # do the matrix math for rotation and translation
        
                matrixList = wTC
                camMatrix = getMetadataMatrix(wTC)
                
                flipZ=nuke.math.Matrix4()
                flipZ.makeIdentity()
                flipZ.scale(1,1,-1)
             
                transposedMatrix = nuke.math.Matrix4(camMatrix)
                transposedMatrix.transpose()
                transposedMatrix=transposedMatrix*flipZ
                invMatrix=transposedMatrix.inverse()
                
                for i in range(0,16):
                    matrixList[i]=invMatrix[i]
                
                for i, v in enumerate( matrixList ):
                    cam[ 'matrix' ].setValueAt( v, frame, i)
            # UPDATE PROGRESS BAR
                task.setProgress( int( float(curTask) / frameRange.frames() *100) )
    except:
        print 'select at least one read node'