###    Advanced CornerPin for easier copying of tracker information
###    
###    ---------------------------------------------------------
###    im_cornerPin.py v2
###    Created: 06/09/2010
###    Modified: 24/09/2010
###    Written by Igor Majdandzic
###    igor@badgerfx.com

import nuke

def cornerPin():
    n = nuke.thisNode()
    mc = methodClass()
        
    #CREATE KNOBS
    tabKnob = nuke.Tab_Knob('Options')
    methodKnob = nuke.Enumeration_Knob( 'method', 'method', ['AdjustCornerPin', 'Copy4PtTrack', 'Link4PtTrack'] )
    methodKnob.setTooltip(tooltips(0))
    stabilizeKnob = nuke.Boolean_Knob('stabilize')
    refFrameKnob = nuke.Int_Knob('refFrame', 'reference frame')
    refFrameKnob.setValue(nuke.Root().firstFrame())
    refFrameKnob.setEnabled(False)
    refFrameKnob.setTooltip(tooltips(1))
    enableRefFrameKnob = nuke.Boolean_Knob('enableRefFrame', '')
    enableRefFrameKnob.setFlag(nuke.ENDLINE)
    updateKnob = nuke.PyScript_Knob( 'update', 'Update', '%s' % mc.initial())

    fromHiddenKnob1 = nuke.XY_Knob('fromH1')
    fromHiddenKnob1.setValue(n['from1'].value())
    fromHiddenKnob1.setFlag(nuke.INVISIBLE)
    fromHiddenKnob2 = nuke.XY_Knob('fromH2')
    fromHiddenKnob2.setValue(n['from2'].value())
    fromHiddenKnob2.setFlag(nuke.INVISIBLE)
    fromHiddenKnob3 = nuke.XY_Knob('fromH3')
    fromHiddenKnob3.setValue(n['from3'].value())
    fromHiddenKnob3.setFlag(nuke.INVISIBLE)
    fromHiddenKnob4 = nuke.XY_Knob('fromH4')
    fromHiddenKnob4.setValue(n['from4'].value())
    fromHiddenKnob4.setFlag(nuke.INVISIBLE)
    
    toHiddenKnob1 = nuke.XY_Knob('toH1')
    toHiddenKnob1.setValue(n['to1'].value())
    toHiddenKnob1.setFlag(nuke.INVISIBLE)
    toHiddenKnob2 = nuke.XY_Knob('toH2')
    toHiddenKnob2.setValue(n['to2'].value())
    toHiddenKnob2.setFlag(nuke.INVISIBLE)
    toHiddenKnob3 = nuke.XY_Knob('toH3')
    toHiddenKnob3.setValue(n['to3'].value())
    toHiddenKnob3.setFlag(nuke.INVISIBLE)
    toHiddenKnob4 = nuke.XY_Knob('toH4')
    toHiddenKnob4.setValue(n['to4'].value())
    toHiddenKnob4.setFlag(nuke.INVISIBLE)
    
    snapKnob = nuke.XY_Knob('imageSize')
    snapKnob.setFlag(nuke.INVISIBLE)
    storeKnob = nuke.XY_Knob('store')
    storeKnob.setFlag(nuke.INVISIBLE)
    for i in (snapKnob, storeKnob):
        i.setValue(n.width(), 0)
        i.setValue(n.height(), 1)
    
    
    #ADD KNOBS
    n.addKnob(tabKnob)
    n.addKnob(methodKnob)
    n.addKnob(stabilizeKnob)
    n.addKnob(refFrameKnob)
    n.addKnob(enableRefFrameKnob)
    n.addKnob(updateKnob)

    n.addKnob(fromHiddenKnob1)
    n.addKnob(fromHiddenKnob2)
    n.addKnob(fromHiddenKnob3)
    n.addKnob(fromHiddenKnob4)
    n.addKnob(toHiddenKnob1)
    n.addKnob(toHiddenKnob2)
    n.addKnob(toHiddenKnob3)
    n.addKnob(toHiddenKnob4)

    n.addKnob(snapKnob)
    n.addKnob(storeKnob)
    
    
    

class methodClass:

    def __init__( self ):
        self.n = nuke.thisNode()
        self.tn = ''
        self.sn = nuke.selectedNodes()
        if len(self.sn) == 2:
            for i in self.sn:
                if i.Class() == 'Tracker3':
                    self.tn = i
    
    def initial( self ):
        return '''n = nuke.thisNode()
if n['method'].value() == 'AdjustCornerPin':
\tim_cornerPin.methodClass().adjustCornerPin()
elif n['method'].value() == 'Copy4PtTrack':
\tim_cornerPin.methodClass().copy4PtTrack()
elif n['method'].value() == 'Link4PtTrack':
\tim_cornerPin.methodClass().link4PtTrack()'''

    def adjustCornerPin( self ):
    
        for i in range(1,5):
            knobFrom = 'from'+str(i)
            knobTo = 'to' + str(i)
            fromValue = self.n.knob(knobFrom).value()
            self.n.knob(knobTo).setValue(fromValue)


    def setReferenceFrame( self ):

        refFrame = self.n['refFrame'].value()

        for i in range(1,5):
            knobFrom = 'fromH'+str(i)
            knobTo = 'toH' + str(i)
            toValue = self.n.knob(knobTo).getValueAt(refFrame)
            self.n.knob(knobFrom).setValue(toValue)
            

    def copy4PtTrack( self ):
        if self.tn == '':
            return nuke.message('Select this cornerpin\nand one tracker node')
        
        for i in range(1,5):
            knobTrack = 'track' + str(i)
            knobTo = 'toH' + str(i)
            trackExpr = '%s.%s' % (self.tn.name(), knobTrack)
            self.n[knobTo].copyAnimations(self.tn[knobTrack].animations())

        label = self.n['label']
                
        if label.value() != '':
            label.setValue('from ' + self.tn.name() + '\n' + label.value())
        else:
            label.setValue('from ' + self.tn['name'].value())
            

        
    def link4PtTrack( self ):
        if self.tn == '':
            return nuke.message('Select this cornerpin\nand one tracker node')
        
        for i in range(1,5):
            knobTrack = 'track' + str(i)
            knobTo = 'toH' + str(i)
            trackExpr = '%s.%s' % (self.tn.name(), knobTrack)
            self.n.knob(knobTo).setExpression(trackExpr)



def cornerPinCB():
    n = nuke.thisNode()
    k = nuke.thisKnob()

    if k.name() in ('from1', 'from2', 'from3', 'from4'):
        index = k.name()[-1]
        
        if k.isAnimated() == True:
            n['fromH%s' % index].setAnimated()
        elif k.isAnimated() == False:
            n['fromH%s' % index].clearAnimated()

        if n['stabilize'].value() == False:
            n['fromH%s' % index].setValue(k.value())
        elif n['stabilize'].value() == True:
            n['toH%s' % index].setValue(k.value())

            
    if k.name() in ('fromH1', 'fromH2', 'fromH3', 'fromH4'):
        index = k.name()[-1]

        if n['stabilize'].value() == False and k.isAnimated() == True:
            n['from%s' % index].copyAnimations(k.animations())

        elif n['stabilize'].value() == False and k.isAnimated() == False:
            n['from%s' % index].setValue(k.value())

        elif n['stabilize'].value() == True and k.isAnimated() == True:
            n['to%s' % index].copyAnimations(k.animations())

        elif n['stabilize'].value() == True and k.isAnimated() == False:
            n['to%s' % index].setValue(k.value())
            

    if k.name() in ('to1', 'to2', 'to3', 'to4'):
        index = k.name()[-1]

        if k.isAnimated() == True:
            n['toH%s' % index].setAnimated()
        elif k.isAnimated() == False:
            n['toH%s' % index].clearAnimated()
            
        if n['stabilize'].value() == False:
            n['toH%s' % index].setValue(k.value())
        elif n['stabilize'].value() == True:
            n['fromH%s' % index].setValue(k.value())
            
    if k.name() in ('toH1', 'toH2', 'toH3', 'toH4'):
        index = k.name()[-1]

        if n['stabilize'].value() == False and k.isAnimated() == True:
            n['to%s' % index].copyAnimations(k.animations())

        elif n['stabilize'].value() == False and k.isAnimated() == False:
            n['to%s' % index].setValue(k.value())

        elif n['stabilize'].value() == True and k.isAnimated() == True:
                n['from%s' % index].copyAnimations(k.animations())

        elif n['stabilize'].value() == True and k.isAnimated() == False:
                n['from%s' % index].setValue(k.value())


    if k.name() == 'stabilize' and k.value() == False:
        for i in range(1,5):
            knobFrom = 'from' + str(i)
            knobTo = 'to' + str(i)
            knobFromH = 'fromH' + str(i)
            knobToH = 'toH' + str(i)
            knobsFrom = [knobFrom, knobFromH]
            knobsTo = [knobTo, knobToH]
            for knob in (knobsFrom, knobsTo):
                if n[knob[0]].isAnimated():
                    n[knob[0]].clearAnimated()  
                if n[knob[1]].isAnimated():
                    n[knob[0]].copyAnimations(n[knob[1]].animations())
                else:
                    n[knob[0]].setValue(n[knob[1]].value())

    elif k.name() == 'stabilize' and k.value() == True:
        for i in range(1,5):
            knobFrom = 'from' + str(i)
            knobTo = 'to' + str(i)
            knobFromH = 'fromH' + str(i)
            knobToH = 'toH' + str(i)
            knobsFrom = [knobFrom, knobToH]
            knobsTo = [knobTo, knobFromH]
            for knob in (knobsFrom, knobsTo):
                if n[knob[0]].isAnimated():
                    n[knob[0]].clearAnimated()  
                if n[knob[1]].isAnimated():
                    n[knob[0]].copyAnimations(n[knob[1]].animations())
                else:
                    n[knob[0]].setValue(n[knob[1]].value())

    if k.name() == 'enableRefFrame':
        if k.value() is True:
            n['refFrame'].setEnabled(True)   
            methodClass().setReferenceFrame()

        elif k.value() is False:
            n['refFrame'].setEnabled(False) 
            
        if n['stabilize'].value() == False:
            for i in range(1,5):
                knobFrom = 'from' + str(i)
                knobFromH = 'fromH' + str(i)

                n[knobFrom].setValue(n[knobFromH].value())

        elif n['stabilize'].value() == True:
            for i in range(1,5):
                knobTo = 'to' + str(i)
                knobToH = 'toH' + str(i)

                n[knobTo].setValue(n[knobToH].value())

            
        elif k.value() is False:
            n['refFrame'].setEnabled(False)

    if k.name() == 'refFrame':
        methodClass().setReferenceFrame()

        if n['stabilize'].value() == False:
            for i in range(1,5):
                knobFrom = 'from' + str(i)
                knobFromH = 'fromH' + str(i)

                n[knobFrom].setValue(n[knobFromH].value())

        elif n['stabilize'].value() == True:
            for i in range(1,5):
                knobTo = 'to%d' % i
                knobFromH = 'fromH%d' % i

                n[knobTo].setValue(n[knobFromH].value())

    if n.width() != n['imageSize'].value(0) or n.height() != n['imageSize'].value(1):
        n['imageSize'].setValue(n.width(), 0)
        n['imageSize'].setValue(n.height(), 1)

        factor = (n['imageSize'].value(0)/n['store'].value(0), n['imageSize'].value(1)/n['store'].value(1))

        for i in range(1,5):
            valueOld = n['fromH%d' % i].value()
            valueNew = []
            valueNew.append(valueOld[0] * factor[0])
            valueNew.append(valueOld[1] * factor[1])
            n['fromH%d' % i].setValue(valueNew)
            print n['fromH%d' % i].value()
        
        n['store'].setValue(n['imageSize'].value())

        if n['stabilize'].value() == False:
            for i in range(1,5):
                knobFrom = 'from%d' % i
                knobFromH = 'fromH%d' % i

                n[knobFrom].setValue(n[knobFromH].value())

        elif n['stabilize'].value() == True:
            for i in range(1,5):
                knobTo = 'to%d' % i
                knobFromH = 'fromH%d' % i

                n[knobTo].setValue(n[knobFromH].value())

   
def tooltips(index):
    if index == 0:
        return '''<i>AdjustCornerPin</i>
Copies values from the From tab to the To tab.
<i>Copy4PtTrack</i>
Select this cornerpin and a tracker node, and the values get copied.
<i>Links4PtTrack</i>
Select this cornerpin and a tracker node, and the values get linked.'''
    
    elif index == 1:
        return 'If enabled, it sets the reference frame, and modifies the <i>From</i> tab'
