#######################################################################################################
#  fastExrStart V1.0 - Date: 08.10.2010 - Created by Jan Oberhauser - jan.oberhauser@gmail.com        #
#  Creates a ready to start Script with Shuffles for each Channel and preset Merges                   #
#  Check for a updateted Version at http://janoberhauser.gute-filme-enden-nie.de                      #
#######################################################################################################


#How to Comp the different Channels
#-------------------------------------
#EXPLANATION:
#You dont have enter the full name of the channel if its called "Thatever_Diffuse_WhatDoIKnow" it is enough to just put "diffuse" (always Lower-Case) 
#in the Channel-Name then its gonna find it. If you have more then one Channel with the same Name-Part you can just use the "notCompNodes"-Variable to
#exclude channels. As Oparation you can just use any Operation the Merge-Node offers, just use exactly the same name (like: plus, mult, scrn, over, ...).
#The Script has two modes. Either it just ignores the defined Comp-Channels if they are not found in the Channels of the Node or it creates a not connected
#Shuffle and Merge anyway to connect them later with other Nodes. So even if the Node just has one Channel, you can still use the Script to make a Basic-Comp
#and then hock-up the other Readers to the shuffels by yourself.
#DESCRIPTION: compNodes = {"FIRST_CHANNEL_NAME":"start::", "SECOND_CHANNEL_NAME":"PARENT_CHANNEL:OPERATION:VALUE", "THIRD_CHANNEL_NAME":"PARENT_CHANNEL:OPERATION:VALUE", .., ..}
#EXAMPLE: starts with the "paint"-Channel, then it "mult" the "diffuse" with "1", then it "plus" the "specular" with "1", then it "plus" the "refl" with "1", then it "mult" the "occlusion" with "0.75"
compNodes = {"paint":"start::", "diffuse":"paint:mult:1", "specular":"diffuse:plus:1", "refl":"specular:plus:1", "occlusion":"refl:mult:0.75"}

#Which Channels should not be found
#-------------------------------------
#EXPLANATION:
#If you have for example more Channels with the same name-parts like "paint", "rotopaint", "carpaint" then you can just type in the
#channls which should not be found   
#DESCRIPTION: notCompNodes = {"FIRST_LAYER":"NOT_TO_BE_FOUND_1:NOT_TO_BE_FOUND_2:NOT_TO_BE_FOUND_3", "SECOND_LAYER":"NOT_TO_BE_FOUND_1"}
notCompNodes = {"paint":"rotopaint:carpaint"}

#Create Not-Found-Channels
#EXPLANATION:
#If this is set to True then it created for each Channel in compNodes a Shuffle, NoOp and Merge node even if it is not found in the EXR-File. This can be useful if
#this Channels come from different Files then the selected one.
createNotFoundChannels = True

#Create the Start-Node to which the EXR-Reader is connected?
createStartNode = True
#Create the NoOp-Node beween the Shuffle and the Merge?
createNoOpNode = True
#Create the Dot-Node beween the NoOp and the Merge?
createDotNode = True

#Show Dot-Label?
showDotLabel = True

#Color of the NoOp-Nodes after the Shuffle-Node
noOpTileColor = 0x9b00ff

#Set the Node-Positon-Offset
nodeXOffset = 180
nodeYOffset = 150

#######################################################################################################
#                                                                                                     #
#              NO CHANGES FROM HERE: (OR JUST IF YOU KNOW WHAT YOU ARE DOING)                         #
#                                                                                                     #
#######################################################################################################

#Find the parent Node
def getParentNode(layer, compNodes, compFound):
	iteration = 0
	parentNode = layer
	while True:
		parentNode = compNodes[parentNode]
		parentNode = parentNode.split(':')[0]
		if parentNode in compFound:
			break

		if parentNode == 'start':
			break

		#Just for the case the compNodes is not set up right
		iteration += 1
		if iteration > 20:
			print "ERROR:\nPLEASE CHECK IF THE NAMES OF THE PARENT-NAMES FIT TO THE LAYER-NAMES"
			parentNode = -1
			break

	return parentNode





#Get selected Nodes
allSelectedNodes = nuke.selectedNodes()

compFound = {}
compFoundInv = {}
nodesOrdered = []

#Find First Node in Order
for object in compNodes:
	if compNodes[object].split(':')[0]  == 'start':
		nodesOrdered.append(object)
		break

#Get Order of Nodes
count = 0
for object in compNodes:
	for object2 in compNodes:
		childNode = compNodes[object2]
		childNode = childNode.split(':')[0]
		if childNode == nodesOrdered[count]:
			nodesOrdered.append(object2)
			count += 1
			break


#Go through all Nodes
for thisNode in allSelectedNodes :
	xPosStart = thisNode['xpos'].getValue()
	yPosStart = thisNode['ypos'].getValue()

	#Get all Layers of the EXR
	allChannels = thisNode.channels()
	allLayers = {}
	for channel in allChannels:
		thisData = str(channel.split('.')[0])
		allLayers.update({thisData:''})	


	#Create the Start-Node
	if createStartNode:
		startNode = nuke.nodes.NoOp(name="Start", tile_color=noOpTileColor)
		startNode.setInput(0, thisNode)
		startNode.setXYpos(int(xPosStart), int(yPosStart+nodeYOffset))
	else:
		startNode = thisNode

	#Go through all Channels
	for layer in allLayers:
		layerLower = layer.lower()

		#Go through all Comp-Nodes
		for compChannel in compNodes:
			compThis = True
			#Look for the Channels to Comp together
			if layerLower.find(compChannel, 0, len(layerLower)) > -1: 
				#Check if there is a NotComp-Information available 
				if compChannel in notCompNodes:
					notNodes = notCompNodes[compChannel].split(':')
					#Go through all informations of this specific Node
					for notNode in notNodes:
						#Check if this Layer matches with the notComp-Information
						if layerLower.find(notNode, 0, len(layer)) > -1:
							#If it matches dont comp them
							compThis = False
							#If already found NotComp-Information stop looking for it 
							break
		
				#Check if it should be comped		
				if compThis == True:
					#Add this layer to the Found-Layers
					compFound.update({compChannel:layer})
					compFoundInv.update({layer:compChannel}) 



	#Go through to create Merge- and Shuffle-Nodes
	mergeCount = -1
	#for layer in compFound:
	nodeNumber = -1


	#If also Not-Found-Channels should be created
	if createNotFoundChannels == True:
		for node in nodesOrdered:
			if node not in allLayers:
				if node not in compFound:
					#newAllLayers.append(node)
					compFound.update({node:node})
					compFoundInv.update({node:node})
	
	#Make a new Layer list with the found-Layers first
	newAllLayers = []
	for node in nodesOrdered:
		if node in compFound:
			newAllLayers.append(compFound[node])
	for layer in allLayers:
		if layer not in newAllLayers:
			newAllLayers.append(layer)

 
	
	#Go through the now ordered list
	for layer in newAllLayers:
		layerLower = layer.lower()
		nodeNumber += 1
		layerOriginal = layer
		if layer in compFoundInv: 
			layer = compFoundInv[layer]
		
		#Create Shuffle-Node
		exec(str(layer) +' = nuke.nodes.Shuffle(name = "' + str(layerOriginal) + '_Shuffel", postage_stamp = True)')
		eval(layer).setXYpos(int(nodeNumber*nodeXOffset+xPosStart), int(yPosStart+2*nodeYOffset))
		#++++++++++++++++++
		if layerOriginal in allLayers:
			eval(layer).setInput(0, startNode)
			eval(layer)['in'].setValue(layerOriginal)
		
		#Create NoOp-Node
		if createNoOpNode:
			noOpNode = nuke.nodes.NoOp(name=layerOriginal, tile_color=noOpTileColor)
			noOpNode.setInput(0, eval(layer))
			noOpNode.setXYpos(int(nodeNumber*nodeXOffset+xPosStart), int(yPosStart+3*nodeYOffset))
			exec(layer + "noOpNode = noOpNode")
		else:
			exec("noOpNode = " + str(layer))
			exec(layer + "noOpNode = " + str(layer))

		#If there is Comp-Information create the Merge
		if layer in compFound:
			#Set Variables to connect Nodes
			exec(layer + " = noOpNode")
			exec(layer + "Merge = noOpNode")

			mergeCount += 1	
			#Split into 0->Parent-Node, 1->Operation, 2->Value
			parameters = compNodes[layer].split(':')
	
			parentNode = getParentNode(layer, compNodes, compFound)
			if parentNode != 'start':
				#Create Merge-Node
				merge = nuke.nodes.Merge(name=str(parameters[1]) + " " + str(layer))
				merge.setXYpos(int(xPosStart), int(mergeCount*nodeYOffset+yPosStart+4*nodeYOffset))
				#Set Values in Merge-Node
				merge['operation'].setValue(parameters[1])
				merge['mix'].setValue(float(parameters[2]))
				exec(layer + "Merge = merge")
				
				if mergeCount > 0 and createDotNode == True:
					#Create Dot-Nodes
					dot = nuke.nodes.Dot(note_font_size=20)
					if showDotLabel:
						dot['label'].setValue(' '+str(layerOriginal))
					dot.setXYpos( int(eval(layer)['xpos'].getValue()+35), int(merge['ypos'].getValue()+3) )			
					dot.setInput(0, eval(layer))
					exec(layer +" = dot")

	
	#After all Nodes are created go through to hock-up Merge-Nodes	
	for layer in compFound:		
		parentNode = getParentNode(layer, compNodes, compFound)
		
		if parentNode != 'start':
			#Set Input A
			exec(layer+"Merge.setInput(1, " + layer + ")")
			#Set Input B
			exec(layer+"Merge.setInput(0, " + str(parentNode) + "Merge" + ")")
