##################
#   USE THIS IN MENU.PY:
#
#  import FovCalculator
#  def addFovCalc():
#      fovCalc = FovCalculator.FovCalculator()
#      return fovCalc.addToPane()
#  nuke.menu('Pane').addCommand( 'Fov Calculator', addFovCalc )
#  nukescripts.registerPanel( 'com.ohufx.FovCalculator', addFovCalc )
##################

from __future__ import with_statement
import math
import nuke
import nukescripts
import os


def focalToFov ( focal, aperture ):
    '''
    Convert focal length and aperture to fov
    '''
    return math.degrees( math.atan2(aperture/2, focal) *2 )

def fovToFocal ( fov, aperture ):
    '''
    Convert fov and aperture to focal length
    '''
    return (aperture/2) / ( math.tan(math.radians(fov/2)) )

def focalToAp ( focal, fov ):
    '''
    Convert focal and fov to aperture
    '''
    return 2 * focal * ( math.tan(math.radians(fov/2)) )

class FovCalculator( nukescripts.PythonPanel ):
    def __init__( self):
        '''Convert focal length, aperture and field of view'''
        nukescripts.PythonPanel.__init__( self, "Fov Calculator","com.ohufx.FovCalculator" )
        #super( FovCalculator, self ).__init__( 'Fov Calculator', 'com.ohufx.FovCalc' )
        modes = ['aperture', 'focal', 'fov']
        self.apDict = {}
        self.getAps()
            
        self.mode = nuke.Enumeration_Knob( 'mode', 'get <img src=":qrc/images/Eyedropper.png">', modes)
        self.mode.setValue( 'fov' )
        self.mode.setTooltip( 'select which value you want to calculate' )
        self.focal = nuke.Double_Knob( 'focal', 'focal length @TargetCamera.png' )
        self.focal.setTooltip( 'focal length in mm' )
        self.focal.setRange( 5, 200 )
        self.focal.setDefaultValue( [50] )
        div1 = nuke.Text_Knob('')
        self.apNames = self.apDict.keys()
        self.apNames.sort()
        self.apNames.insert( 0, 'custom')
        self.apList = nuke.Enumeration_Knob( 'ap', 'aperture @Grid.png', self.apNames )
        self.apList.setTooltip( 'select a preset to fill in the filmback dimensions to the right. These values are read from any "apertures.txt" found in the plugin path.\
                                The syntax of the apertures.txt should ismply be "name width height".' )
        self.haperture = nuke.Double_Knob( 'haperture', '' )
        self.haperture.setTooltip( 'width in mm of the film back or chip' )
        if not self.apDict:
            self.apList.setVisible( False )
        self.haperture.clearFlag( nuke.STARTLINE )
        self.haperture.clearFlag( 2 )
        self.haperture.setRange( 0.1, 50 )
        self.haperture.setValue( 24.576 )
        self.vaperture = nuke.Double_Knob( 'vaperture', '' )
        self.vaperture.setTooltip( 'height in mm of the film back or chip' )
        self.vaperture.clearFlag( nuke.STARTLINE )
        self.vaperture.clearFlag( 2 )
        self.vaperture.setRange( 0.1, 50 )
        self.vaperture.setValue( 18.672 )
        
        self.hfov = nuke.Double_Knob( 'hfov', 'horizontal fov @hfov.png' )
        self.hfov.setTooltip( 'horizontal field of view aka "angle of view"' )
        self.hfov.setRange( 10, 180 )
        self.hfov.setValue( focalToFov( self.focal.value(), self.haperture.value() ) )
        self.hfov.setEnabled( False )
        self.vfov = nuke.Double_Knob( 'vfov', 'vertical fov @vfov.png' )
        self.vfov.setTooltip( 'vertical field of view aka "angle of view"' )
        self.vfov.setRange( 10, 180 )
        self.vfov.setValue( focalToFov( self.focal.value(), self.vaperture.value() ) )
        self.vfov.setEnabled( False )
        self.useVert = nuke.Boolean_Knob( 'useVert', 'use vertical' )
        self.useVert.setTooltip( 'if checked, the vertical aperture and fov are used to calucltae the focla length. If off the gorizontal values are used.' )
        
        div2 = nuke.Text_Knob('')
        self.driveCam = nuke.Boolean_Knob( 'driveCam', '<img src=":qrc/images/Roto/CloneToolbar.png"> Drive Existing Camera')
        self.driveCam.setTooltip( 'When checked the camera with the given name will be temprarily linked to the value sin this panel.\
                                  This is handy to do visual checks while tweaking tha panel\'s parameters.\
                                  If a camera node is selected when the checkbox is activated, it\'s name is automatically filled in to the text filed to the right.'
                                  )
        self.driveCam.setFlag( nuke.STARTLINE )
        self.driveCamName = nuke.String_Knob( 'driveCamName', '')
        self.driveCamName.setTooltip( 'name of the camera in the DAG to drive with the above values. This can be manually filled in but is also automatically filled based on the current selection when the checkbox on the left is activated.' )
        self.driveCamName.clearFlag( nuke.STARTLINE )
        self.createCam = nuke.PyScript_Knob( 'createCam', '@Camera.png Create New Camera')
        self.createCam.setTooltip( 'create a new cmeara node with the current values.' )
        
        for k in ( self.mode, self.useVert, div1, self.focal, self.apList, self.haperture, self.vaperture, self.hfov, self.vfov, div2, self.createCam, self.driveCam, self.driveCamName ):
            self.addKnob( k )

        self.useVert.setVisible( False )

    def getAps( self ):
        for d in nuke.pluginPath():
            # FIND apertures.txt IN PLUGIN PATH
            apFile = os.path.join( d, 'apertures.txt')
            if not os.path.isfile( apFile ):
                continue
            # READ THE FILE
            with open( apFile ) as FILE:
                #apString = FILE.read()
                apInfo = FILE.readlines()
            for ap in apInfo:
                self.apDict[ ' '.join( ap.split()[:-2] ) ] = [ float(n) for n in ap.split()[-2:] ]
        
        
    def vertVis( self ):
        for k in ( self.haperture, self.hfov ):
            k.setEnabled( not self.useVert.value() )
        for k in ( self.vaperture, self.vfov ):
            k.setEnabled( self.useVert.value() )

    def apertureAdjust( self, lock ):
        if lock == 'fov':
            self.hfov.setValue( focalToFov( self.focal.value(), self.haperture.value() ) )
            self.vfov.setValue( focalToFov( self.focal.value(), self.vaperture.value() ) )
        if lock == 'focal':
            if self.useVert.value():
                self.focal.setValue( fovToFocal( self.vfov.value(), self.vaperture.value() ) )
            else:
                self.focal.setValue( fovToFocal( self.hfov.value(), self.haperture.value() ) )
                
    def createCamFn( self ):
        nuke.createNode( 'Camera2',\
                 'focal %s haperture %s vaperture %s' % (\
                     self.focal.value(),\
                    self.haperture.value(),\
                    self.vaperture.value() ))

    def driveApList( self ):
        for k, v in self.apDict.iteritems():
            if v == [self.haperture.value(), self.vaperture.value()]:
                # PRESET FOUND
                self.apList.setValue( k )
                try:
                    self.apNames.remove( 'custom' )
                except ValueError:
                    pass
                self.apList.setValues( self.apNames )
                break
            else:
                # NO PRESET FOUND, USE CUSTOM
                if not 'custom' in self.apNames:
                    self.apNames.insert( 0, 'custom' )
                self.apList.setValues( self.apNames )
                self.apList.setValue( 'custom' )


    def driveCamFn( self ):
        if self.driveCam.value():
            with nuke.root():
                cam = nuke.toNode( self.driveCamName.value() )
            cam['haperture'].setValue( self.haperture.value() )
            cam['vaperture'].setValue( self.vaperture.value() )
            cam['focal'].setValue( self.focal.value() )

    def knobChanged( self, knob ):
        lock = self.mode.value()
        if knob is self.mode:
            icons = [ '@Grid.png', '@Camera.png', '@TargetCamera.png' ]
            for k in ( self.haperture, self.vaperture, self.focal, self.hfov, self.vfov ):
                k.setEnabled( not k.name().endswith( knob.value() ) )
                self.useVert.setVisible( knob.value() == 'focal' )
            self.apList.setEnabled( not knob.value().endswith( 'aperture') )
            if knob.value() == 'focal':
                self.vertVis()

        if knob is self.useVert:
            self.vertVis()
            if self.useVert.value():
                self.focal.setValue( fovToFocal( self.vfov.value(), self.vaperture.value() ) )
            else:
                self.focal.setValue( fovToFocal( self.hfov.value(), self.haperture.value() ) )

        if knob is self.focal:
            if lock == 'aperture':
                self.haperture.setValue( focalToAp( self.focal.value(), self.hfov.value() ) )
                self.vaperture.setValue( focalToAp( self.focal.value(), self.vfov.value() ) )
            if lock == 'fov':
                self.hfov.setValue( focalToFov( self.focal.value(), self.haperture.value() ) )
                self.vfov.setValue( focalToFov( self.focal.value(), self.vaperture.value() ) )

        if knob is self.apList:
            try:
                self.haperture.setValue( self.apDict[ knob.value() ][0])
                self.vaperture.setValue( self.apDict[ knob.value() ][1])
                self.apertureAdjust( lock )
            except KeyError:
                pass
            
        if knob.name().endswith( 'aperture' ):
            self.apertureAdjust( lock )
            self.driveApList()

        if knob.name().endswith( 'fov' ):
            if lock == 'focal':
                if self.useVert.value():
                    self.focal.setValue( fovToFocal( self.vfov.value(), self.vaperture.value() ) )
                else:
                    self.focal.setValue( fovToFocal( self.hfov.value(), self.haperture.value() ) )
            if lock == 'aperture':
                self.haperture.setValue( focalToAp( self.hfov.value(), self.hfov.value() ) )
                self.vaperture.setValue( focalToAp( self.vfov.value(), self.vfov.value() ) )

        if knob is self.createCam:
            self.createCamFn()

        camNodes = [ nn for nn in nuke.selectedNodes() if len( set( ['haperture', 'vaperture', 'focal'] ).intersection( set( nn.knobs().keys() ) ) ) == 3]
        if knob is self.driveCam:
            self.driveCamName.setEnabled( knob.value() )
            if camNodes:
                if knob.value():
                    self.driveCamName.setValue( camNodes[0].name() )
                    self.driveCamFn()
                    

        if knob.name() in ('haperture', 'vaperture', 'focal', 'hfov', 'vfov'):
            self.driveCamFn()
            

            
