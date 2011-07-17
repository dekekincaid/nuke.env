import nuke
def selectedValue():
    inputBox = nuke.Panel("SetValueSelected")
    inputBox.addSingleLineInput("Class", "Blur")
    inputBox.addSingleLineInput("Knob", "size")
    inputBox.addSingleLineInput("Value", "10")
    inputBox.show()

    sClass = inputBox.value("Class")
    sKnob = inputBox.value("Knob")
    sVal = inputBox.value("Value")

    f = float(sVal)
    
    for i in nuke.selectedNodes():
        if i.Class() == sClass:
            i.knob(sKnob).setValue(f)