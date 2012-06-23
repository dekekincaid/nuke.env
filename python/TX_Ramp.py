##################################################################	
## BUTTONS
##################################################################	
import nuke

def addLine():
	n = nuke.thisNode()
	pCount = n['pCounter'].value()
	id = getId()
	dicValues = createDicValues(pCount)

	deleteKnobs(pCount)
	addItem(id, dicValues, pCount)
	pCount = n['pCounter'].value()
	createLines(dicValues, id, pCount)
	createRamp()


def removeLine():
	n = nuke.thisNode()
	pCount = n['pCounter'].value()
	id = getId()
	dicValues = createDicValues(pCount)

	deleteKnobs(pCount)
	removeItem(id, dicValues,pCount)
	pCount = n['pCounter'].value()
	createLines(dicValues, id, pCount)
	createRamp()

##################################################################	

## Get ID of the button
def getId():
	thisAddBT = nuke.thisKnob().name()
	if thisAddBT == 'start_add':
		id = 0
	else:
		id = int(thisAddBT.strip('p_adremov'))
	return id


## Create list of values
def createDicValues(pCount):
	n = nuke.thisNode()
	dicValues = []

	# values of each pXXX knobs
	if pCount>0:
		for i in range(pCount):
			color = n['p%03d_color' % (i+1)].value()
			position = n['p%03d' % (i+1)].value()
			dicTmp = {'color':color, 'position':position}
	
			dicValues.append(dicTmp)
		
	# value of end knobs
	color = n['end_color'].value()
	position = (n.width(), 50)
	dicEnd = {'color':color, 'position':position}
	
	dicValues.append(dicEnd)
	
	return dicValues
	
	
## Delete knobs
def deleteKnobs(pCount):
	n = nuke.thisNode()
	if pCount>0 :
		for i in range(int(pCount)):
			for j in ['p%03d_color' % (i + 1), 'p%03d' % (i + 1), 'p%03d_add' % (i + 1), 'p%03d_remove' % (i + 1)]:
				n.removeKnob(n[j])
	for i in ['end_color', 'end', 'end_add', 'end_remove']:
		nuke.thisNode().removeKnob(n[i])
		

	
## Add item to the list
def addItem(id, dicValues,pCount):
	n = nuke.thisNode()
	if id == 0:
		item = { 'color':[0.0,0.0,0.0,0.0], 'position': (dicValues[0]['position'][0]/2, 50.0) }
	else :
		item = { 'color':[0.0,0.0,0.0,0.0], 'position': ((dicValues[id-1]['position'][0]+dicValues[id]['position'][0])/2, 50) }
	dicValues.insert(id, item)
	n['pCounter'].setValue(int(pCount+1))
	return dicValues
	

## Remove item of the list
def removeItem(id, dicValues,pCount):
	n = nuke.thisNode()
	dicValues.pop(id-1)
	n['pCounter'].setValue(int(pCount-1))
	if n['pCounter'].value() < 0:
		n['pCounter'].setValue(0)
	return dicValues
	

## Create line
def createLines(dicValues,id,pCount):
	## Variables
	n = nuke.thisNode()
	addPath = '<img src=":qrc/images/Add.png">'
	removePath = '<img src=":qrc/images/Remove.png">'

	for i in range(int(pCount)):
		## Create knobs
		col = nuke.AColor_Knob('p%03d_color' % (i + 1), '%03d' % (i + 1))
		col.setValue(dicValues[i]['color'])
		pos = nuke.XY_Knob('p%03d' % (i + 1), 'position')
		pos.clearFlag(0x1000)
		pos.setValue(dicValues[i]['position'])
		addLine = nuke.PyScript_Knob('p%03d_add' % (i + 1), addPath)
		addLine.setValue('TX_Ramp.addLine()')
		remLine = nuke.PyScript_Knob('p%03d_remove' % (i + 1), removePath)
		remLine.setValue('TX_Ramp.removeLine()')
		
		## Create knobs
		n.addKnob(col)
		n.addKnob(pos)
		n.addKnob(addLine)
		n.addKnob(remLine)
		
	## Create end knobs
	col = nuke.AColor_Knob('end_color', '  end')
	col.setValue(dicValues[-1]['color'])
	pos = nuke.XY_Knob('end', 'position')
	pos.clearFlag(0x1000)
	pos.setValue(dicValues[-1]['position'])
	pos.setFlag(0x00000080)
	pos.setFlag(0x00008000)
	addLine = nuke.PyScript_Knob('end_add',addPath)
	addLine.setFlag(0x00000080)
	remLine = nuke.PyScript_Knob('end_remove',removePath)
	remLine.setFlag(0x00000080)
	
	## Create end knobs
	n.addKnob(col)
	n.addKnob(pos)
	n.addKnob(addLine)
	n.addKnob(remLine)


## Create Ramp
def createRamp():
	## Variables
	n = nuke.thisNode()
	pCount = n['pCounter'].value()


	## Create ramp expressions
	if pCount == 0:
		n.begin()
		nuke.toNode('COLORAMA')['expr0'].setValue( '(1-x/width)*start_color.r  + x/width*end_color.r' )
		nuke.toNode('COLORAMA')['expr1'].setValue( '(1-x/width)*start_color.g  + x/width*end_color.g' )
		nuke.toNode('COLORAMA')['expr2'].setValue( '(1-x/width)*start_color.b  + x/width*end_color.b' )
		nuke.toNode('COLORAMA')['expr3'].setValue( '(1-x/width)*start_color.a  + x/width*end_color.a' )
		n.end()
	
	else :
		n.begin()
		rampExpr = ''

		for i in range(int(pCount)):
			## Variables
			pt_i  = 'p%03d.x' % (i+1)
			
			if i == 0 :
				pt_im = 'start.x'
			else :
				pt_im = 'p%03d.x'  % (i)	
				
			if i+1 == pCount:
				pt_ip = 'end.x'
			else :
				pt_ip = 'p%03d.x' % (i+2)
			
			c_i  = 'p%03d_color' % (i+1)
			if i == 0 :
				c_im = 'start_color'
			else :
				c_im = 'p%03d_color' % (i)	
				
			if i+1 == pCount:
				c_ip = 'end_color'
			else :
				c_ip = 'p%03d_color' % (i+2)
	
	
			#expression =  'x>=' + pt_im + ' && x<' + pt_i + '? (1-x/(' + pt_i + '-' + pt_im + '))*' + c_im + '.%s + x/(' + pt_i + '-' + pt_im + ')*' + c_i + '.%s  : x>=' + pt_i + ' && x<' + pt_ip + '? (1-x/(' + pt_ip + '-' + pt_i + '))*' + c_i + '.%s + x/(' + pt_ip + '-' + pt_i + ')*' + c_ip + '.%s  : '
			expression =  'x>=' + pt_im + ' && x<' + pt_i + '? (1-(x-' + pt_im + ')/(' + pt_i + '-' + pt_im + '))*' + c_im + '.%s + (x-' + pt_im + ')/(' + pt_i + '-' + pt_im + ')*' + c_i + '.%s  : x>=' + pt_i + ' && x<' + pt_ip + '? (1-(x-' + pt_i + ')/(' + pt_ip + '-' + pt_i + '))*' + c_i + '.%s + (x-' + pt_i + ')/(' + pt_ip + '-' + pt_i + ')*' + c_ip + '.%s  : '
		
			rampExpr = rampExpr + expression
		
		rampExpr = rampExpr + ' 0'
	
		## Set expressions
		for i in range(4):
			chan = ['r', 'g', 'b', 'a']
			nuke.toNode('COLORAMA')['expr'+ str(i)].setValue(rampExpr.replace('%s', chan[i]))

		n.end()

