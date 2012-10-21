import nuke
import random
import colorsys

def autobackdropRandomColor():
  '''
  Automatically puts a backdrop behind the selected nodes.

  The backdrop will be just big enough to fit all the select nodes in, with room
  at the top for some text in a large font.
  '''
  selNodes = nuke.selectedNodes()
  if not selNodes:
    return nuke.nodes.BackdropNode()

  # Calculate bounds for the backdrop node.
  bdX = min([node.xpos() for node in selNodes])
  bdY = min([node.ypos() for node in selNodes])
  bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
  bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

  # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
  left, top, right, bottom = (-10, -80, 10, 10)
  bdX += left
  bdY += top
  bdW += (right - left)
  bdH += (bottom - top)

  #better random color option I stole from Ben Dickson post on listserve 
  h = random.randrange(90, 270) / 360.0
  s = random.randrange(1, 75) / 100.0
  v = 0.25
  r,g,b = colorsys.hsv_to_rgb(h, s, v)
  rcolor = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,255),16)

  n = nuke.nodes.BackdropNode(xpos = bdX,
                              bdwidth = bdW,
                              ypos = bdY,
                              bdheight = bdH,
                              tile_color = rcolor,
                              note_font_size=42)

  # revert to previous selection
  n['selected'].setValue(False)
  for node in selNodes:
    node['selected'].setValue(True)

  return n
