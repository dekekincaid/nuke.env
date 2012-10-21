#
# readList.py
#
# Cameron Carson [cameron.a.carson@gmail.com]
#
# designed to grab all the filenames from read nodes and populate a text node with them for a zero frame.
# 
#

import nukescripts
import nuke
import re
import os
import sys
from glob import glob

def makereadList():
	if nuke.toNode("ReadList"):
		nuke.message("ReadList already Exists!")
		return
	dupList = []
	readList = "\n"
	for n in nuke.allNodes():
		currentnode = n
		classname = currentnode.Class()
		if classname == "Read":
			print currentnode['name'].value()
			filename = nuke.filename(currentnode)
			splitDirs = filename.split("/")
			dirName = splitDirs[-1]
			dupList.append(dirName)
	dupList = list(set(dupList))
	for l in dupList:
		readList = readList+l+"\n"
	t = nuke.createNode("Text")
	t.setName("ReadList")
	t['message'].setValue(readList)
	t["size"].setValue(32)
	t["box"].setX(50)
	t["box"].setY(50)
	t["box"].setR(1870)
	t["box"].setT(1030)
	o = t["opacity"]
	o.setAnimated()
	o.setValueAt(1,0)
	o.setValueAt(0,1)
	
	#Creates SetThisFrame button
	tabName = nuke.Tab_Knob("Update_Read_List", "UpdateReadList")
	t.addKnob(tabName)
	scriptButton = nuke.PyScript_Knob("UpdateReadList", "UpdateReadList", "readList.updatereadList()")
	t.addKnob(scriptButton)
	
def updatereadList():
	if nuke.toNode("ReadList"):
		readList = "\n"
		for n in nuke.allNodes():
			currentnode = n
			classname = currentnode.Class()
			if classname == "Read":
				print currentnode['name'].value()
				filename = nuke.filename(currentnode)
				splitDirs = filename.split("/")
				dirName = splitDirs[-1]
				readList = readList+dirName+"\n"
		t = nuke.toNode("ReadList")
		t["message"].setValue(readList)