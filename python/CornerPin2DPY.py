#Little script created by Pau Rocher Castellano
###############bikura@gmail.com################



def CornerPin2DPY(modo):

  n = nuke.thisNode()
  copy = n['varCopy']

  #read values of the knobs
  to1a = n["to1"].value(0)
  to1b = n["to1"].value(1)
  to2a = n["to2"].value(0)
  to2b = n["to2"].value(1)
  to3a = n["to3"].value(0)
  to3b = n["to3"].value(1)
  to4a = n["to4"].value(0)
  to4b = n["to4"].value(1)

  from1a = n["from1"].value(0)
  from1b = n["from1"].value(1)
  from2a = n["from2"].value(0)
  from2b = n["from2"].value(1)
  from3a = n["from3"].value(0)
  from3b = n["from3"].value(1)
  from4a = n["from4"].value(0)
  from4b = n["from4"].value(1)


  if modo == 0 :
  #Set values from "from" to "to"
    n["to1"].setValue(from1a, 0)
    n["to1"].setValue(from1b, 1)

    n["to2"].setValue(from2a, 0)
    n["to2"].setValue(from2b, 1)

    n["to3"].setValue(from3a, 0)
    n["to3"].setValue(from3b, 1)

    n["to4"].setValue(from4a, 0)
    n["to4"].setValue(from4b, 1)

  elif modo == 1 :
  #Set values from "to" to "from"
    n["from1"].setValue(to1a, 0)
    n["from1"].setValue(to1a, 1)

    n["from2"].setValue(to2a, 0)
    n["from2"].setValue(to2b, 1)

    n["from3"].setValue(to3a, 0)
    n["from3"].setValue(to3b, 1)

    n["from4"].setValue(to4a, 0)
    n["from4"].setValue(to4b, 1)

  elif modo == 2 :
  #Invert values
    n["to1"].setValue(from1a, 0)
    n["to1"].setValue(from1b, 1)

    n["to2"].setValue(from2a, 0)
    n["to2"].setValue(from2b, 1)

    n["to3"].setValue(from3a, 0)
    n["to3"].setValue(from3b, 1)

    n["to4"].setValue(from4a, 0)
    n["to4"].setValue(from4b, 1)

    n["from1"].setValue(to1a, 0)
    n["from1"].setValue(to1b, 1)

    n["from2"].setValue(to2a, 0)
    n["from2"].setValue(to2b, 1)

    n["from3"].setValue(to3a, 0)
    n["from3"].setValue(to3b, 1)

    n["from4"].setValue(to4a, 0)
    n["from4"].setValue(to4b, 1)

  elif modo == 3 :
  #Copy values from "from"
    to1a = to1a
    copy.setValue(1)
    bufferCtrl(0, nuke.frame())

    n["buf1"].setValue(from1a, 0)
    n["buf1"].setValue(from1b, 1)

    n["buf2"].setValue(from2a, 0)
    n["buf2"].setValue(from2b, 1)

    n["buf3"].setValue(from3a, 0)
    n["buf3"].setValue(from3b, 1)

    n["buf4"].setValue(from4a, 0)
    n["buf4"].setValue(from4b, 1)

  elif modo == 4 :
  #Copy values from "to"
    to1a = to1a
    copy.setValue(2)
    bufferCtrl(1, nuke.frame())

    n["buf1"].setValue(to1a, 0)
    n["buf1"].setValue(to1b, 1)

    n["buf2"].setValue(to2a, 0)
    n["buf2"].setValue(to2b, 1)

    n["buf3"].setValue(to3a, 0)
    n["buf3"].setValue(to3b, 1)

    n["buf4"].setValue(to4a, 0)
    n["buf4"].setValue(to4b, 1)

  elif modo == 5 :
  #Paste values to "from"
    if copy.value() == 2 :
      n["from1"].setValue(to1a, 0)
      n["from1"].setValue(to1b, 1)

      n["from2"].setValue(to2a, 0)
      n["from2"].setValue(to2b, 1)

      n["from3"].setValue(to3a, 0)
      n["from3"].setValue(to3b, 1)

      n["from4"].setValue(to4a, 0)
      n["from4"].setValue(to4b, 1)
    elif copy.value() == 1 :
      n["from1"].setValue(from1a, 0)
      n["from1"].setValue(from1b, 1)

      n["from2"].setValue(from2a, 0)
      n["from2"].setValue(from2b, 1)

      n["from3"].setValue(from3a, 0)
      n["from3"].setValue(from3b, 1)

      n["from4"].setValue(from4a, 0)
      n["from4"].setValue(from4b, 1)
    else:
      nuke.message("First copy some values!")
      

  elif modo == 6 :
  #Paste values to "to"
    if copy.value() == 1 :
      n["to1"].setValue(from1a, 0)
      n["to1"].setValue(from1b, 1)

      n["to2"].setValue(from2a, 0)
      n["to2"].setValue(from2b, 1)

      n["to3"].setValue(from3a, 0)
      n["to3"].setValue(from3b, 1)

      n["to4"].setValue(from4a, 0)
      n["to4"].setValue(from4b, 1)
    elif copy.value() == 2 :
      n["to1"].setValue(to1a, 0)
      n["to1"].setValue(to1b, 1)

      n["to2"].setValue(to2a, 0)
      n["to2"].setValue(to2b, 1)

      n["to3"].setValue(to3a, 0)
      n["to3"].setValue(to3b, 1)

      n["to4"].setValue(to4a, 0)
      n["to4"].setValue(to4b, 1)
    else:
      nuke.message("First copy some values!")


  elif modo == 7 :
  #Set key to "from"
    anTo = n["from1"].animations()
    if anTo == [] :
      ask = nuke.ask ("There is no animation. Do you want to create it?")
      if ask == False:
        pass
      else:
        #creates animation curve for the knobs
	from1a_ani = n["from1"].setAnimated(0)
	from1b_ani = n["from1"].setAnimated(1)
	from2a_ani = n["from2"].setAnimated(0)
	from2b_ani = n["from2"].setAnimated(1)
	from3a_ani = n["from3"].setAnimated(0)
	from3b_ani = n["from3"].setAnimated(1)
	from4a_ani = n["from4"].setAnimated(0)
	from4b_ani = n["from4"].setAnimated(1)

	#reads animation curve
        nuke.AnimationCurve.setKey(n["from1"].animations()[0], nuke.frame(), from1a)
        nuke.AnimationCurve.setKey(n["from1"].animations()[1], nuke.frame(), from1b)
        nuke.AnimationCurve.setKey(n["from2"].animations()[0], nuke.frame(), from2a)
        nuke.AnimationCurve.setKey(n["from2"].animations()[1], nuke.frame(), from2b)
        nuke.AnimationCurve.setKey(n["from3"].animations()[0], nuke.frame(), from3a)
        nuke.AnimationCurve.setKey(n["from3"].animations()[1], nuke.frame(), from3b)
        nuke.AnimationCurve.setKey(n["from4"].animations()[0], nuke.frame(), from4a)
        nuke.AnimationCurve.setKey(n["from4"].animations()[1], nuke.frame(), from4b)

    else:
      nuke.AnimationCurve.setKey(n["from1"].animations()[0], nuke.frame(), from1a)
      nuke.AnimationCurve.setKey(n["from1"].animations()[1], nuke.frame(), from1b)
      nuke.AnimationCurve.setKey(n["from2"].animations()[0], nuke.frame(), from2a)
      nuke.AnimationCurve.setKey(n["from2"].animations()[1], nuke.frame(), from2b)
      nuke.AnimationCurve.setKey(n["from3"].animations()[0], nuke.frame(), from3a)
      nuke.AnimationCurve.setKey(n["from3"].animations()[1], nuke.frame(), from3b)
      nuke.AnimationCurve.setKey(n["from4"].animations()[0], nuke.frame(), from4a)
      nuke.AnimationCurve.setKey(n["from4"].animations()[1], nuke.frame(), from4b)


  elif modo == 8 :
  #Set key to "to"
    anTo = n["to1"].animations()
    if anTo == [] :
      ask = nuke.ask ("There is no animation. Do you want to create it?")
      if ask == False:
        pass
      else:
        #creates animation curve for the knobs
	to1a_ani = n["to1"].setAnimated(0)
	to1b_ani = n["to1"].setAnimated(1)
	to2a_ani = n["to2"].setAnimated(0)
	to2b_ani = n["to2"].setAnimated(1)
	to3a_ani = n["to3"].setAnimated(0)
	to3b_ani = n["to3"].setAnimated(1)
	to4a_ani = n["to4"].setAnimated(0)
	to4b_ani = n["to4"].setAnimated(1)

	#sets keyframe
        nuke.AnimationCurve.setKey(n["to1"].animations()[0], nuke.frame(), to1a)
        nuke.AnimationCurve.setKey(n["to1"].animations()[1], nuke.frame(), to1b)
        nuke.AnimationCurve.setKey(n["to2"].animations()[0], nuke.frame(), to2a)
        nuke.AnimationCurve.setKey(n["to2"].animations()[1], nuke.frame(), to2b)
        nuke.AnimationCurve.setKey(n["to3"].animations()[0], nuke.frame(), to3a)
        nuke.AnimationCurve.setKey(n["to3"].animations()[1], nuke.frame(), to3b)
        nuke.AnimationCurve.setKey(n["to4"].animations()[0], nuke.frame(), to4a)
        nuke.AnimationCurve.setKey(n["to4"].animations()[1], nuke.frame(), to4b)

    else:
      #sets keyframe
      nuke.AnimationCurve.setKey(n["to1"].animations()[0], nuke.frame(), n["to1"].value(0))
      nuke.AnimationCurve.setKey(n["to1"].animations()[1], nuke.frame(), n["to1"].value(1))
      nuke.AnimationCurve.setKey(n["to2"].animations()[0], nuke.frame(), n["to2"].value(0))
      nuke.AnimationCurve.setKey(n["to2"].animations()[1], nuke.frame(), n["to2"].value(1))
      nuke.AnimationCurve.setKey(n["to3"].animations()[0], nuke.frame(), n["to3"].value(0))
      nuke.AnimationCurve.setKey(n["to3"].animations()[1], nuke.frame(), n["to3"].value(1))
      nuke.AnimationCurve.setKey(n["to4"].animations()[0], nuke.frame(), n["to4"].value(0))
      nuke.AnimationCurve.setKey(n["to4"].animations()[1], nuke.frame(), n["to4"].value(1))

def bufferCtrl(source, frame):
  n = nuke.thisNode()
  if source == 0 :
    n['in_buffer'].setValue("in buffer: FROM, from frame " + str (frame))
  else:
    n['in_buffer'].setValue("in buffer: TO, from frame " + str (frame))




