# Duplicate Geometry 1.0
#
# This script creates some 3D transform nodes for a 3D geometry and a control node.
# (C) Copyright: Adrian Heinzel ( adrian.heinzel@rtt.ag ) 2010-09-09


import nuke
import random

def DuplicateGeometry():
	for n in nuke.selectedNodes():
		if n.Class() == "Cube" or n.Class() == "Card2" or n.Class() == "Cylinder" or n.Class() == "Sphere" or n.Class() == "ReadGeo2":
			
			class dialog(object):
				window = nuke.Panel("Duplicate Geometry")
				window.addSingleLineInput("Clones:", 10)
			
			dialogResult = dialog.window.show()
			
			if dialogResult == 1:
				nuke.tprint("Duplicating Geometry...")
			else:
				nuke.tprint("Canceled")
				return None
			
			nodeYPos = n.ypos()
			nodeXPos = n.xpos()
			
			controlNode = nuke.createNode("NoOp")
			controlNode.knob("name").setValue("DuplicateGeometry")
			controlNode.knob('xpos').setValue(nodeXPos + 150)
			controlNode.knob('ypos').setValue(nodeYPos)
			
			controlNode.addKnob(nuke.Tab_Knob('Controls'))
			
			code = 'import random\nfor a in range(%s):\n a += 1\n TKnob = \"Translate_\" + str(a)\n RKnob = \"Rotate_\" + str(a)\n SKnob = \"Scale_\" + str(a)\n nuke.toNode(\"DuplicateGeometry\").knob(TKnob).setValue(random.uniform(-1, 1), 0)\n nuke.toNode(\"DuplicateGeometry\").knob(TKnob).setValue(random.uniform(-1, 1), 1)\n nuke.toNode(\"DuplicateGeometry\").knob(TKnob).setValue(random.uniform(-1, 1), 2)\n nuke.toNode(\"DuplicateGeometry\").knob(RKnob).setValue(random.uniform(-1, 1), 0)\n nuke.toNode(\"DuplicateGeometry\").knob(RKnob).setValue(random.uniform(-1, 1), 1)\n nuke.toNode(\"DuplicateGeometry\").knob(RKnob).setValue(random.uniform(-1, 1), 2)\n nuke.toNode(\"DuplicateGeometry\").knob(SKnob).setValue(random.uniform(-1, 1), 0)\n nuke.toNode(\"DuplicateGeometry\").knob(SKnob).setValue(random.uniform(-1, 1), 1)\n nuke.toNode(\"DuplicateGeometry\").knob(SKnob).setValue(random.uniform(-1, 1), 2)' % int(dialog.window.value("Clones:"))

			controlNode.addKnob(nuke.PyScript_Knob('Randomize', 'Randomize', code))
			
			controlNode.addKnob(nuke.XYZ_Knob('Translate'))
			controlNode.addKnob(nuke.XYZ_Knob('Rotate'))
			controlNode.addKnob(nuke.XYZ_Knob('Scale'))
			
			controlNode.addKnob(nuke.XYZ_Knob('TranslateRandom'))
			controlNode.addKnob(nuke.XYZ_Knob('RotateRandom'))
			controlNode.addKnob(nuke.XYZ_Knob('ScaleRandom'))
			
			for a in range(int(dialog.window.value("Clones:"))):
				a += 1
				TKnob = "Translate_" + str(a)
				RKnob = "Rotate_" + str(a)
				SKnob = "Scale_" + str(a)
				controlNode.addKnob(nuke.XYZ_Knob(TKnob))
				controlNode.addKnob(nuke.XYZ_Knob(RKnob))
				controlNode.addKnob(nuke.XYZ_Knob(SKnob))
				
				controlNode.knob(TKnob).setVisible(bool(0))
				controlNode.knob(RKnob).setVisible(bool(0))
				controlNode.knob(SKnob).setVisible(bool(0))
				
				controlNode.knob(TKnob).setValue(random.uniform(-1, 1), 0)
				controlNode.knob(TKnob).setValue(random.uniform(-1, 1), 1)
				controlNode.knob(TKnob).setValue(random.uniform(-1, 1), 2)
				controlNode.knob(RKnob).setValue(random.uniform(-1, 1), 0)
				controlNode.knob(RKnob).setValue(random.uniform(-1, 1), 1)
				controlNode.knob(RKnob).setValue(random.uniform(-1, 1), 2)
				controlNode.knob(SKnob).setValue(random.uniform(-1, 1), 0)
				controlNode.knob(SKnob).setValue(random.uniform(-1, 1), 1)
				controlNode.knob(SKnob).setValue(random.uniform(-1, 1), 2)
			
			scene = nuke.createNode("Scene")
			scene.knob('xpos').setValue(nodeXPos + 300)
			scene.knob('ypos').setValue(nodeYPos + 150)
			nuke.extractSelected()
			
			for i in range(int(dialog.window.value("Clones:"))):
				transform = nuke.createNode("TransformGeo")
				nuke.extractSelected()
				transform.knob('xpos').setValue(nodeXPos + 150)
				transform.knob('ypos').setValue(nodeYPos + (150 * (i + 1)))
				transform.setInput(0, n)
				
				scene.setInput(i, transform)
				
				vTranslate_0 = "DuplicateGeometry.Translate * " + str(i + 1) + " + DuplicateGeometry.TranslateRandom * DuplicateGeometry.Translate_" + str(i + 1)
				vTranslate_1 = "DuplicateGeometry.Translate * " + str(i + 1) + " + DuplicateGeometry.TranslateRandom * DuplicateGeometry.Translate_" + str(i + 1)
				vTranslate_2 = "DuplicateGeometry.Translate * " + str(i + 1) + " + DuplicateGeometry.TranslateRandom * DuplicateGeometry.Translate_" + str(i + 1)
				vRotate_0 = "DuplicateGeometry.Rotate * " + str(i + 1) + " + DuplicateGeometry.RotateRandom * DuplicateGeometry.Rotate_" + str(i + 1)
				vRotate_1 = "DuplicateGeometry.Rotate * " + str(i + 1) + " + DuplicateGeometry.RotateRandom * DuplicateGeometry.Rotate_" + str(i + 1)
				vRotate_2 = "DuplicateGeometry.Rotate * " + str(i + 1) + " + DuplicateGeometry.RotateRandom * DuplicateGeometry.Rotate_" + str(i + 1)
				vScale_0 = "1 + DuplicateGeometry.Scale * " + str(i + 1) + " + DuplicateGeometry.ScaleRandom * DuplicateGeometry.Scale_" + str(i + 1)
				vScale_1 = "1 + DuplicateGeometry.Scale * " + str(i + 1) + " + DuplicateGeometry.ScaleRandom * DuplicateGeometry.Scale_" + str(i + 1)
				vScale_2 = "1 + DuplicateGeometry.Scale * " + str(i + 1) + " + DuplicateGeometry.ScaleRandom * DuplicateGeometry.Scale_" + str(i + 1)
				
				transform.knob("translate").setExpression(vTranslate_0, 0)
				transform.knob("translate").setExpression(vTranslate_1, 1)
				transform.knob("translate").setExpression(vTranslate_2, 2)
				transform.knob("rotate").setExpression(vRotate_0, 0)
				transform.knob("rotate").setExpression(vRotate_1, 1)
				transform.knob("rotate").setExpression(vRotate_2, 2)
				transform.knob("scaling").setExpression(vScale_0, 0)
				transform.knob("scaling").setExpression(vScale_1, 1)
				transform.knob("scaling").setExpression(vScale_2, 2)