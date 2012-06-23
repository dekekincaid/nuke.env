import nuke

def iFilterCreate():
  a = nuke.selectedNode ()
#info  //  flag al numero de steps //  amagar knobs de la pestanya2
  a.knob("info").setValue ("iFilter currently empty")
  a.knob('Steps').setFlag(600)
  a.knob('iFilterFilter').setFlag(1024)
  a.knob('iFilterBlur').setFlag(1024)
  a.knob('iFilterQuality').setFlag(1024)
  a.knob('iFilterBlurFilter').setFlag(1024)
  a.knob('iFilterBlurQuality').setFlag(1024)
  a.knob('iFilterDefAspect').setFlag(1024)
  a.knob('iFilterDefScaling').setFlag(1024)
  a.knob('iFilterDefQuality').setFlag(1024)
  a.knob('iFilterDefMethod').setFlag(1024)
  a.knob('previousAmount').setFlag(1024)

def iFilter03(filter, steps, previousAmount):
##########
##asigne el node actual a la variable "a"

  a = nuke.thisNode ()

##########
##lectura dels knobs

  steps = int (steps)
  stepVal = float (1/float (steps))

  diler = float (nuke.value ("Amount"))
  dilerDiv = float (diler/steps)

  filter = nuke.Enumeration_Knob.value(a.knob ("Filter"))

##########
##empythonament dels nodes que fan falta

  inMask = nuke.toNode ("puntazoMask")
  inImage = nuke.toNode ("puntazo")

##empythonament dels nodes que fan falta
##########


##########
##Borra els nodes existents
  id = int(previousAmount)
  idKill = 0
  for i in range (id):
      idKill = idKill+1
####Expressions
      nomExpr = "idilerExpr" + str (idKill)
      killExpr = nuke.toNode (nomExpr)
      nuke.delete (killExpr)
####Blurs
      nomBlr = "idilerBlur" + str (idKill)
      killBlr = nuke.toNode (nomBlr)
      nuke.delete (killBlr)
####Erodes
      nomEro = "idilerErode" + str (idKill)
      killEro = nuke.toNode (nomEro)
      nuke.delete (killEro)
####Keymixes
      nomKey = "idilerKeymix" + str (idKill)
      killKey = nuke.toNode (nomKey)
      nuke.delete (killKey)
####BlurBlurs
      nomKey = "idilerErode" + str (idKill)
      killKey = nuke.toNode (nomKey)
      nuke.delete (killKey)
####Defocus
      nomKey = "idilerErode" + str (idKill)
      killKey = nuke.toNode (nomKey)
      nuke.delete (killKey)
  primerKey = nuke.toNode ("KeymixInicik")
  nuke.delete (primerKey)

##########
##Amaga ensenya knobs
  if filter == "dilerFast":
    a.knob('iFilterFilter').setFlag(1024)
    a.knob('iFilterBlur').setFlag(1024)
    a.knob('iFilterQuality').setFlag(1024)
    a.knob('iFilterBlurFilter').setFlag(1024)
    a.knob('iFilterBlurQuality').setFlag(1024)
    a.knob('iFilterDefAspect').setFlag(1024)
    a.knob('iFilterDefScaling').setFlag(1024)
    a.knob('iFilterDefQuality').setFlag(1024)
    a.knob('iFilterDefMethod').setFlag(1024)
    a.knob('previousAmount').setFlag(1024)

  elif filter == "dilerFilter":
    a.knob('iFilterFilter').clearFlag(1024)
    a.knob('iFilterBlur').setFlag(1024)
    a.knob('iFilterQuality').setFlag(1024)
    a.knob('iFilterBlurFilter').setFlag(1024)
    a.knob('iFilterBlurQuality').setFlag(1024)
    a.knob('iFilterDefAspect').setFlag(1024)
    a.knob('iFilterDefScaling').setFlag(1024)
    a.knob('iFilterDefQuality').setFlag(1024)
    a.knob('iFilterDefMethod').setFlag(1024)
    a.knob('previousAmount').setFlag(1024)

  elif filter == "dilerBlur":
    a.knob('iFilterFilter').setFlag(1024)
    a.knob('iFilterBlur').clearFlag(1024)
    a.knob('iFilterQuality').clearFlag(1024)
    a.knob('iFilterBlurFilter').setFlag(1024)
    a.knob('iFilterBlurQuality').setFlag(1024)
    a.knob('iFilterDefAspect').setFlag(1024)
    a.knob('iFilterDefScaling').setFlag(1024)
    a.knob('iFilterDefQuality').setFlag(1024)
    a.knob('iFilterDefMethod').setFlag(1024)
    a.knob('previousAmount').setFlag(1024)

  elif filter == "blur":
    a.knob('iFilterFilter').setFlag(1024)
    a.knob('iFilterBlur').setFlag(1024)
    a.knob('iFilterQuality').setFlag(1024)
    a.knob('iFilterBlurFilter').clearFlag(1024)
    a.knob('iFilterBlurQuality').clearFlag(1024)
    a.knob('iFilterDefAspect').setFlag(1024)
    a.knob('iFilterDefScaling').setFlag(1024)
    a.knob('iFilterDefQuality').setFlag(1024)
    a.knob('iFilterDefMethod').setFlag(1024)
    a.knob('previousAmount').setFlag(1024)

  elif filter == "defocus":
    a.knob('iFilterFilter').setFlag(1024)
    a.knob('iFilterBlur').setFlag(1024)
    a.knob('iFilterQuality').setFlag(1024)
    a.knob('iFilterBlurFilter').setFlag(1024)
    a.knob('iFilterBlurQuality').setFlag(1024)
    a.knob('iFilterDefAspect').clearFlag(1024)
    a.knob('iFilterDefScaling').clearFlag(1024)
    a.knob('iFilterDefQuality').clearFlag(1024)
    a.knob('iFilterDefMethod').clearFlag(1024)
    a.knob('previousAmount').setFlag(1024)

##########
##Creacio dels nodes

  xXpresionPos = 100
  ide = 0


  for i in range (steps) :
      ide = ide + 1
####Expressions
      nom = "idilerExpr" + str (ide)
      b = "name " + nom + " temp_name0 r" + str (ide) + " temp_expr0 step(r," + str (stepVal*ide) + ")" +" expr0 r" + str (ide) + " xpos " + str (xXpresionPos*ide) + " ypos 100"
      nom = nuke.createNode ("Expression", b, False)
      nom.setInput (0, inMask)

####Blurs
      nomBlur = "idilerBlur" + str (ide)
      bl = "name " + nomBlur + " size parent.Soften" + " xpos " + str (xXpresionPos*ide) + " ypos 150"
      blr = nuke.createNode ("Blur", bl, False)
      blr.setInput (0, nom)

####Filtres

      if filter == "dilerFast":
          nomErode = "idilerErode" + str(ide)
          valDiler = float (dilerDiv*ide)
          siz = "parent.Amount/" + str(steps) + "*" + str(ide)
          er = "name " + nomErode + " channels all " +  " size " + siz + " xpos " + str (xXpresionPos*ide) + " ypos 500"
          ero = nuke.createNode ("Dilate", er, False)
          ero.setInput (0, inImage)

      elif filter == "dilerFilter":
          nomErode = "idilerErode" + str (ide)
          valDiler = float (dilerDiv*ide)
          siz = "parent.Amount/" + str(steps) + "*" + str(ide)
          er = "name " + nomErode + " channels all " +  " size " + siz + " filter {{parent.iFilterFilter}} xpos " + str (xXpresionPos*ide) + " ypos 500"
          ero = nuke.createNode ("FilterErode", er, False)
          ero.setInput (0, inImage)

      elif filter == "dilerBlur":
          nomErode = "idilerErode" + str (ide)
          valDiler = float (dilerDiv*ide)
          siz = "parent.Amount/" + str(steps) + "*" + str(ide)
          er = "name " + nomErode + " channels all " +  " size " + siz + " blur {{parent.iFilterBlur}} quality {{parent.iFilterQuality}} xpos " + str (xXpresionPos*ide) + " ypos 500"
          ero = nuke.createNode ("Erode", er, False)
          ero.setInput (0, inImage)

      elif filter == "blur":
          nomErode = "idilerErode" + str (ide)
          valDiler = float (dilerDiv*ide)
          siz = "parent.Amount/" + str(steps) + "*" + str(ide)
          er = "name " + nomErode + " channels all " +  " size " + siz + " filter {{parent.iFilterBlurFilter}} quality {{parent.iFilterBlurQuality}} xpos " + str (xXpresionPos*ide) + " ypos 500"
          ero = nuke.createNode ("Blur", er, False)
          ero.setInput (0, inImage)

      elif filter == "defocus":
          nomErode = "idilerErode" + str (ide)
          valDiler = float (dilerDiv*ide)
          siz = "parent.Amount/" + str(steps) + "*" + str(ide)
          er = "name " + nomErode + " channels all " +  " defocus " + siz + " ratio {{parent.iFilterDefAspect}} scale {{parent.iFilterDefScaling}} quality {{parent.iFilterDefQuality}} method {{iFilterDefMethod}} xpos " + str (xXpresionPos*ide) + " ypos 500"
          ero = nuke.createNode ("Defocus", er, False)
          ero.setInput (0, inImage)

####Keymix
  ide = 0
  for i in range (steps):
      ide = ide + 1
      bl = nuke.toNode ("idilerBlur" + str(ide-1))
      er = nuke.toNode ("idilerErode" + str (ide))
      ke = "name idilerKeymix" + str (ide) + " maskChannel rgba.red xpos " + str (xXpresionPos*ide) + " ypos 550"
      creaKey = nuke.createNode ( "Keymix", ke, False)
      creaKey.setInput (2, bl)
      creaKey.setInput (0, er)

      creaKeyMenysU = "idilerKeymix" + str (ide-1)
      creaKeyAnterior = nuke.toNode (creaKeyMenysU)
      creaKey.setInput (1, creaKeyAnterior)
########Primer Keymix
  km1 = nuke.toNode ("idilerKeymix1")
  er1 = nuke.toNode ("idilerErode1")
  km1.setInput (0, er1)
  km1.setInput (1, inImage)
  km1.setInput (2, blr)

####conect l'output i el switch al ultim keymix
  out = nuke.toNode ("iFilterFinalMerge")
  iFilterSwitch = nuke.toNode ('iFilterSwitch')
  out.setInput (1, creaKey)
  iFilterSwitch.setInput (0, creaKey)
    
####Fora del loop reposiciono els ultims nodes d'expressio i de Blur pa posar-los al comensament i que els cables no es creuin
  nom.knob("xpos").setValue (-10)
  nom.knob("ypos").setValue (100)

  blr.knob("xpos").setValue (-10)
  blr.knob("ypos").setValue (150)

####info
  a.knob("info").setValue (".:  Current filter: "+str(filter)+" with "+str(int(float(steps)))+" steps  (Click button to update ...) :.")




def knobChanged():
  n = nuke.thisNode()
  k = nuke.thisKnob()
  filter = n["Filter"].value()
  steps = n['Steps'].value()
  previousAmount = n['previousAmount'].value()
 
  if k.name() == 'Steps':
    iFilter03 (filter, steps, previousAmount)
    
#nuke.addKnobChanged (knobChanged, nodeClass='Group')
nuke.removeKnobChanged (knobChanged, nodeClass='Group')
