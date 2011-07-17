###############################################################################################################
##
## by alex.bigott@circlesandlines.com
##
## select a read node and run missingFrames()


import nuke
import os

###############################################################################################################
##
## find the missing frames in a given read node and return them

def missingFrames():
	
	missingFiles = []
	completeFileName = ""
	
	# first check if a node is selected and if so if it is a read node
	selectedNodes = nuke.selectedNodes()
	
	# either nothing or too much is selected
	if (len(selectedNodes) != 1):
		nuke.message("This only works if you select one Read node!")
		return "Fail"
	
	nodeType = selectedNodes[0].Class()
	
	if (nodeType != "Read"):
		nuke.message("This only works if you select one Read node!")
		return "Fail"
		
	#now we are sure one read node is selected, so go on.
	
	readNode = selectedNodes[0]
	
	fileNameLong = readNode.knob("file").value()
	startFrame = readNode.knob("first").value()
	endFrame = readNode.knob("last").value()
	
	# split the long file name with path to its subsections	
	splitFileNameLong = os.path.split(fileNameLong)
	fileNameShort = splitFileNameLong[1]
	pathName = splitFileNameLong[0]
	splitFileName = fileNameShort.split(".")
	
	if (len(splitFileName) != 3):
		nuke.message("File does not have the format name.number.ext.\nSearch the missing frames yourself :)")
		return "Fail"
		
	fileName = splitFileName[0]
	filePaddingOrg = splitFileName[1]
	filePaddingLength = len((filePaddingOrg) % 0)
	fileExtension = splitFileName[2]
	
	
	# now with all that given information search for missing files in the sequence 
	for i in range(startFrame, endFrame+1):
		# first build the string of the padded frameNumbers
		frameNumber = str(i)		
		
		while(len(frameNumber) < filePaddingLength):
			frameNumber = "0" + frameNumber
			
		completeFileName = pathName + "/" + fileName + "." + frameNumber + "." + fileExtension
		
		if not os.path.isfile(completeFileName):
			missingFiles.append(i)
	
	if(len(missingFiles) == 0):
		nuke.message("No file seems to be missing")
		return
			
	cleanedUpMissingFiles = cleanUpList(missingFiles)
	
	nuke.message("In the frame range: " + str(startFrame) + "-" + str(endFrame) + "\nThe following files are missing:\n\n" + cleanedUpMissingFiles)
	
	return
			
	
	
##############################################################################################################
##
## from a sequencial array create a readable list which is returned

def cleanUpList(missingFrames):

	cleanMissingFrames = []
	missingFramesNice = ""
	dirtySize = 0
	minV = 0
	maxV = 0
	
	dirtySize = len(missingFrames)
	
	minV = missingFrames[0]
	maxV = missingFrames[0]

	for i in range(dirtySize):
		if (missingFrames[i] == (maxV+1)):
			#as long as the frames are in sequence, update the maxV value
			maxV = missingFrames[i]
		else:
			#if not in sequence, set the values
			cleanMissingFrames.append(minV)
			cleanMissingFrames.append(maxV)
			minV = maxV = missingFrames[i];

		if (i == (dirtySize-1)):
			#write the values if the list is at the end
			cleanMissingFrames.append(minV)
			cleanMissingFrames.append(maxV)
			
	for i in range(2,len(cleanMissingFrames),2):
		# create the formated output of the frames in the window for the user to shorten the list
		if(cleanMissingFrames[i] == cleanMissingFrames[i+1]):
			missingFramesNice += (str)(cleanMissingFrames[i]) + ", "
		else:
			missingFramesNice += (str)(cleanMissingFrames[i]) + "-" + (str)(cleanMissingFrames[i+1]) + ", "


	return missingFramesNice
