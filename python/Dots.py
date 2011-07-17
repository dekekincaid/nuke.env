import nuke
def Dots():
    selected = nuke.selectedNode()
    selectedX = selected.xpos()
    selectedY = selected.ypos()
    selectedW = selected.screenWidth()
    selectedH = selected.screenHeight()
    A = selected.input(0)
    AX = A.xpos()
    AY = A.ypos()
    AW = A.screenWidth()
    AH = A.screenHeight()
    B = selected.input(1)
    Dot = nuke.nodes.Dot()
    if B:
        BX = B.xpos()
        BY = B.ypos()
        BW = B.screenWidth()
        BH = B.screenHeight()
        Dot.setInput(0,B)
        selected.setInput(1,Dot)
        Dot.setXYpos(BX+BW/2-6,selectedY+4)
        if A.Class()== "Dot":
            selected.knob("xpos").setValue(AX-selectedW/2+6)
        else:        
            selected.knob("xpos").setValue(AX)
###################################################
    else:
        Dot.setInput(0,A)
        selected.setInput(0,Dot)        
        Dot.setXYpos(selectedX+selectedW/2-6,AY+AH/2-6)   
###################################################



