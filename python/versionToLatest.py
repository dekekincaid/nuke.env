#
# versionToLatest.py
#
# Cameron Carson [cameron.a.carson@gmail.com]
#
# Designed to replace the stock /"Version to Latest" function that will only update if the files are sequentially numbered.
# This Script will search the directory of your shot sequences and then look for ones with the same read name. It then substitutes the highest version it finds for the one in your read node.
#

import nukescripts
import nuke
import re
import os
import sys
from glob import glob

def versionToLatest():
	for n in nuke.selectedNodes():
		currentnode = n
		classname = currentnode.Class()
		if classname == "Read":
			print currentnode['name'].value()
			filename = nuke.filename(currentnode)
			splitDirs = filename.split("/")
			fileDir = ""
			t=0
			dirDepth = len(splitDirs)-2
			for i in splitDirs:
				if t < dirDepth:
					fileDir = fileDir+i+"/"
					t = t+1
			dirName = splitDirs[-2]
			dirPath = fileDir+dirName
			
			def sameName(path1, path2):
				if noVer(path1) == noVer(path2):
					return True
				return False
			
			def pathVer(path):
				return re.search( r'_[vV]\d+', path).group(0)
			
			def noVer(path):
				splitPath = re.split( r'_[vV]\d+', path)
				if len(splitPath) >= 2:
					noVer = splitPath[0]+splitPath[1]
				else:
					noVer = splitPath[0]
				return noVer
			
			versionDict = {}
			versionDict["seqs"] = []
			for d in os.listdir( fileDir ):
				path = os.path.join( fileDir, d)
				if os.path.isdir( path ):
					if sameName(dirPath, path):
						versionDict["seqs"].append(path)
			maxVer = pathVer(max(versionDict["seqs"]))
				
			newFilename = filename.replace(pathVer(filename), maxVer)
			currentnode['file'].setValue(newFilename)
			
			print "\""+dirName+"\" Replaced With... \""+dirName.replace(pathVer(filename), maxVer)+"\""
			
			newdirPath = dirPath.replace(pathVer(filename), maxVer)
			
			def getFileSeq( dirPath ):
				dirName = os.path.basename( dirPath )
				# COLLECT ALL FILES IN THE DIRECTORY THAT HAVE THE SAME NAME AS THE DIRECTORY
				files = glob( os.path.join( dirPath, '%s_*.*' % dirName ) )
				# GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
				firstString = re.findall( r'\d+', files[0] )[-1]
				# GET THE PADDING FROM THE AMOUNT OF DIGITS
				padding = len( firstString )
				# CREATE PADDING STRING FRO SEQUENCE NOTATION
				paddingString = '%02s' % padding
				# CONVERT TO INTEGER
				first = int( firstString )
				# GET LAST FRAME
				last = int( re.findall( r'\d+', files[-1] )[-1] )
				print "first frame = ", first
				print "last frame = ", last
				currentnode['first'].setValue(first)
				currentnode['last'].setValue(last)
				currentnode['origfirst'].setValue(first)
				currentnode['origlast'].setValue(last)
				return
			
			getFileSeq(newdirPath)
	return