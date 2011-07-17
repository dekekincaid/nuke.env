""" 
	flame connect beta for foundry nuke.
	tested under nuke for mac 32 and 64 bit 6.1v1 and 6.1v3. this script is still under development
	altough it seems to run smooth even in large scenes (tested with 800 nodes on DAG).
	this is my first script ever for nuke so you need to know that there may be bugs of which I am 
	not aware of. 
	you can test this script, optimize it, give it to others and have fun with it but if you than 
	give some credits I would be thankful.
	
	copyright, jaden, nov 2010
"""



import nuke


def nukeSelectedNode():
	
	sn = nuke.selectedNode()
	snx = nuke.selectedNode().xpos()
	sny = nuke.selectedNode().ypos()
	allValues = [[snx,sny]]
	return allValues


def searchAreaY():
	sampleArea = nukeSelectedNode()[0]
	a = sampleArea[0]
	b = sampleArea[1]

	sampleAreaMO = [a,b-10]
	sampleAreaMU = [a,b+10]
		
	ro1 = range(sampleAreaMU[0],sampleAreaMO[0])
	ro2 = range(sampleAreaMO[1],sampleAreaMU[1])
	
	ro1.extend(ro2)
	return ro1

def searchAreaX():
	sampleArea = nukeSelectedNode()[0]
	a = sampleArea[0]
	b = sampleArea[1]

	sampleAreaML = [a-40,b]
	sampleAreaMR = [a+40,b]
	
	ro3 = range(sampleAreaML[0],sampleAreaMR[0])
	ro4 = range(sampleAreaML[1],sampleAreaMR[1])
	ro4.extend(ro3)
	return ro4
	
	
def testen ():
	sn = nuke.selectedNode()
	if sn.input(0) and sn.maxInputs() > 2 and not sn.Class() == "Scene" or sn.input(0) and sn.maxInputs() == 2 and not sn.knob("maskChannelInput") and not sn.Class() == "Scene":	
		s = sn.input(0)
		nan = nuke.allNodes()
		tester = 0
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						if s is not tmp:
							sn.setInput(1,tmp)
					
							if tmp.Class() == "Camera2" and sn.Class() == "ScanlineRender":
								sn.setInput(2,tmp)
							else:
								pass
							if tmp.Class() == "Camera" and sn.Class() == "ScanlineRender":
								sn.setInput(2,tmp)
							else:
								pass
							if tmp.Class() == "Scene" and sn.Class() == "ScanlineRender":
								sn.setInput(1,tmp)
							else:
								pass
							if tmp.Class() == "ReadGeo2" and sn.Class() == "ScanlineRender":
								sn.setInput(1,tmp)
							else:
								pass
							if tmp.Class() == "Axis2" and sn.Class() == "TransformGeo":
								sn.setInput(1,tmp)
							else:
								pass
							if tmp.Class() == "Camera2" and sn.Class() == "TransformGeo":
								sn.setInput(2,tmp)
							else:
								pass
							if tmp.Class() == "Camera2" and sn.Class() == "Card3D":
								sn.setInput(1,tmp)
							else:
								pass
							if tmp.Class() == "Axis2" and sn.Class() == "Card3D":
								sn.setInput(2,tmp)
							else:
								pass
							if tmp.Class() == "Camera2" and sn.Class() == "Reconcile3D":
								sn.setInput(1,tmp)
							else:
								pass
							if tmp.Class() == "Axis2" and sn.Class() == "Reconcile3D":
								sn.setInput(2,tmp)
							else:
								pass
							if tmp.Class() == "Camera2" and sn.Class() == "PointsTo3D":
								sn.setInput(1,tmp)
							else:
								pass
						
						else:
					 		pass
	elif sn.input(1) and sn.maxInputs() > 2 and not sn.Class() == "Scene" or sn.input(0) and sn.maxInputs() == 2 and not sn.knob("maskChannelInput") and not sn.Class() == "Scene":	
		nan = nuke.allNodes()
		tester = 0
		t = sn.input(1).name()
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						if t is not c:
							sn.setInput(0,tmp)
						else: 
							pass
	elif sn.Class() == "Scene" and sn.input(0) and not sn.input(1):	
		nan = nuke.allNodes()
		tester = 0
		s = sn.input(0)
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						if s is not tmp:
							sn.setInput(1,tmp)
						else:
							pass
							
	elif sn.Class() == "Scene" and sn.input(0) and sn.input(1) and not sn.input(2):	
		nan = nuke.allNodes()
		tester = 0
		s = sn.input(0)
		t = sn.input(1)
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						if s is not tmp and t is not tmp:
							sn.setInput(2,tmp)
						else:
							pass

	elif sn.Class() == "Scene" and sn.input(0) and sn.input(1) and sn.input(2):	
		nan = nuke.allNodes()
		tester = 0
		s = sn.input(0)
		t = sn.input(1)
		u = sn.input(2)
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						if s is not tmp and t is not tmp and u is not tmp:
							sn.setInput(3,tmp)
						else:
							pass

	elif sn.Class() == "Scene" and sn.input(0) and sn.input(1) and sn.input(2) and not sn.input(3):	
		nan = nuke.allNodes()
		tester = 0
		
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			s = sn.input(0)
			t = sn.input(1)
			u = sn.input(2)
			v = sn.input(3)
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						if s is not tmp and t is not tmp and u is not tmp and v is not tmp:
							sn.setInput(4,tmp)
						else:
							pass



	else:
		nan = nuke.allNodes()
		tester = 0
		for x in nan:
			a = [x.xpos()]
			b = [x.ypos()]
			c = x.name()
			
			for y in a:
				if y in searchAreaX():
					tester = tester + 1
				
				else: 
					tester = 0
				for z in b:
					if z in searchAreaY():
						tester = tester + 1
					
					else:
						tester = 0
					
					if tester == 2 or tester == 4:
						sn = nuke.selectedNode()
						tmp = nuke.toNode(c)
						sn.setInput(0,tmp)
						if tmp.Class() == "Camera2" and sn.Class() == "ScanlineRender":
							sn.setInput(2,tmp)
						else:
							pass
						if tmp.Class() == "Camera" and sn.Class() == "ScanlineRender":
							sn.setInput(2,tmp)
						else:
							pass
						if tmp.Class() == "Scene" and sn.Class() == "ScanlineRender":
							sn.setInput(1,tmp)
						else:
							pass
						if tmp.Class() == "ReadGeo2" and sn.Class() == "ScanlineRender":
							sn.setInput(1,tmp)
						else:
							pass
						if tmp.Class() == "Axis2" and sn.Class() == "TransformGeo":
							sn.setInput(1,tmp)
						else:
							pass
						if tmp.Class() == "Camera2" and sn.Class() == "TransformGeo":
							sn.setInput(2,tmp)
						else:
							pass
						if tmp.Class() == "Camera2" and sn.Class() == "Card3D":
							sn.setInput(1,tmp)
						else:
							pass
						if tmp.Class() == "Axis2" and sn.Class() == "Card3D":
							sn.setInput(2,tmp)
						else:
							pass
						if tmp.Class() == "Camera2" and sn.Class() == "Reconcile3D":
							sn.setInput(1,tmp)
						else:
							pass
						if tmp.Class() == "Axis2" and sn.Class() == "Reconcile3D":
							sn.setInput(2,tmp)
						else:
							pass
						if tmp.Class() == "Camera2" and sn.Class() == "PointsTo3D":
							sn.setInput(1,tmp)
						else:
							pass
						
					else:
				 		pass
