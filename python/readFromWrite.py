# Read node generator v1.2, 2011-11-21
# by Fredrik Averpil, fredrik.averpil [at] gmail.com, www.averpil.com/fredrik
# 
#
# Usage: select any Write node and run readFromWrite() after having sourced this file, or put the following in your menu.py:
# import writeNode
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Write node generator', 'writeNode.writeNode()', 'shift+w' )
# 
# 



import nuke
import os
import re


def searchForInString(string, searchPattern):
	# Look for %04d
	reMatch = re.search(searchPattern, string)
	# if reMatch:
		# print('reMatch for ' + string + ': ' + str(reMatch) )
	
	return reMatch




def checkForFileKnob():
	try:
		selectedNodeFilePath = nuke.selectedNode()['file'].getValue()
		error = False
	except ValueError:
		error = True
		nuke.message('No (Write) node selected.')
	except NameError:
		error = True
		nuke.message('You must select a Write node.')
	
	return error




# Creates a Read node from the selected Write node
def readFromWrite():

	# Check for a file knob...
	error = checkForFileKnob()


	# If a Write node has been selected, let's go on!
	if not error:


		# Grab the interesting stuff from the write node and double check we actually selected a Write node...
		selectedNodeName = nuke.selectedNode().name()
		selectedNodeFilePath = nuke.selectedNode()['file'].getValue()
		selectedNodePremult = str( nuke.selectedNode()['premultiplied'].getValue() )
		selectedNodeXpos = nuke.selectedNode().xpos()
		selectedNodeYpos = nuke.selectedNode().ypos()

		# Split filepath into list
		filePathSplitted = str.split( selectedNodeFilePath, '/' )

		# Get filetype
		filePathSplittedDots = str.split( selectedNodeFilePath, '.' )
		filetype = filePathSplittedDots[len(filePathSplittedDots)-1]
		
		filePath = ''
		# File path to write node's target folder
		for i in range(0,len(filePathSplitted)-1):
			filePath = filePath + filePathSplitted[i] + '/'

		# Filename taken from Write node
		filename = filePathSplitted[ len(filePathSplitted)-1 ]

		# Debug
		# print('Write node says: ' + filename)

		# Let's look for #### or %04d
		searchPattern = '(#+)|(%\d\d?d)'
		frameRangeFound = searchForInString(filename, searchPattern)

		# If framerange was not found we assume we are dealing with a movie file or a single image file
		if not frameRangeFound:
			# Create the read node
			node = nuke.createNode( "Read", "file "+selectedNodeFilePath )
			
			# Nicely placement of nodes
			node.setXpos( selectedNodeXpos )
			node.setYpos( selectedNodeYpos + 60)

			# Was it premultiplied?
			node.knob('premultiplied').fromScript( selectedNodePremult )
		


		# If framerange was found, we need to start getting clever
		else:

			# Split the filname into what's before and after the framerange
			sourcePrefix, sourceSuffix = filename.split('.%04d.')

			# Debug
			# print('We are looking for: ' + sourcePrefix + ' of type ' + filetype)
			# print('Look for them in directory: ' + filePath)

			
			# See if we can list the folder's files
			if os.path.exists( nuke.callbacks.filenameFilter(filePath) ):
				# List the contents of the folder
				files = os.listdir( nuke.callbacks.filenameFilter(filePath) )
			else:
				nuke.message('Folder path not found:\n' + filePath)
				error = True


			# Setting some defaults
			framerangeFound = False
			firstFrame = 'Not set'
			lastFrame = 'Not set'
			fileFound = False



			if error == False:
				
				for file in files:

					# Search for the occurance of a four digit number surrounded by period signs
					reMatch = re.search('\.[0-9][0-9][0-9][0-9]\.', file)
					if reMatch:
						# print('reMatch for ' + file + ': ' + str(reMatch) + ': ' + reMatch.group(0) )				
						targetPrefix, targetSuffix = file.split(reMatch.group(0))

						if sourcePrefix == targetPrefix:
							fileFound = True
							framerangeFound = True	
							# print(file + ' seems to be related to filename ' + sourcePrefix + '.####.' + sourceSuffix)

							dump, frame, dump = reMatch.group(0).split('.')

							if firstFrame == 'Not set':
								firstFrame = frame
							else:
								lastFrame = frame



				if fileFound == True:

					# Change %04d to ####
					selectedNodeFilePath = str.replace(selectedNodeFilePath, '%04d', '####')

					# Create the Read node
					node = nuke.createNode( "Read", "file " + selectedNodeFilePath)

					# Check for framerange, and if not found use the frameranges from the project settings
					if framerangeFound == False:
						# Long shot guess for framerange (from settings)
						firstFrame = str(int(nuke.root()['first_frame'].getValue()))
						lastFrame = str(int(nuke.root()['last_frame'].getValue()))
						node.knob('first').fromScript(firstFrame)
						node.knob('last').fromScript(lastFrame)

					# Set the framerange
					node.knob('first').fromScript(firstFrame)
					node.knob('last').fromScript(lastFrame)

					# Nicely placement of nodes
					node.setXpos( selectedNodeXpos )
					node.setYpos( selectedNodeYpos + 60)

					# Was it premultiplied?
					node.knob('premultiplied').fromScript( selectedNodePremult )
		

					# Debug
					# print('Read node created for ' + filename)
				


				# Some warning messages

				# If the Write node has not rendered any files to load
				if fileFound == False:
					nuke.message('Render file/s not found, seems like you forgot to render them out.')

				# If no framerange was found from an image sequence
				elif framerangeFound == False:
					nuke.message('I was unable to figure out the frame range and guessed it was ' + firstFrame + '-' + lastFrame + ', based on the project settings. Please check it manually.')