###  Little script created by PauRocher & CucoBurés to launch a flipbook from
###  a file sequence in the HDisk from Nuke
#
#
###  put this file in your plugins path and the following line in your menu.py
###  nuke.load("flipbookfromdisk.py");
###  nuke.load ("flipbookfromdisk.py")
###  m.addCommand("Flipbook from Disk", "flipbookfromdisk()", "")


def flipbookfromdisk():
  import nukescripts
  open = nuke.getClipname ("choose a sequence, man")
  openSplit = open.split (" ")
  inout = openSplit [1].split ("-")
  fframe = "first 20"
  container = nuke.createNode ("Read", "name flipbook file " + openSplit[0] + " first " + inout[0] + " last " + inout[1] , True)
  nukescripts.framecycler_this(container, inout[0], inout[1] , 1)
  nuke.delete (container)