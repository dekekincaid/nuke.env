#!/usr/bin python
#
# nukeprocess 
# Written by Francois Lord, technical director at ObliqueFX - me@francoislord.com
# version 0.8
# Documentation and more inf at:
# http://francoislord.com/blog/computer-graphics/nuke/nukeprocess_74
#
# copyright 2009 Francois Lord
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#     <http://www.gnu.org/licenses/>.

import sys
import os
import os.path
import subprocess
import base64
import bz2
import pickle


class NukeProcess(object):
	"""Provides easy control over Nuke's processing abilities from the exterior"""

	def __init__(self, sInFilename, iStartFrame, iEndFrame, iStep = 1, **kwargs):

		# Modify these locations to your facility's default.
		if sys.platform.startswith('win'):
			self._nukeExe = r"C:\Program Files\The Foundry\Nuke5.1v5\Nuke5.1.exe"
		else:
			self._nukeExe = "//usr/local/Nuke5.1v5/Nuke5.1"

		# You might want to add some custom Python liraries you have so that Nuke can access them.
		# I have set to our own one, you should replace this.
		self.script = '''
			import nuke, sys
			if sys.platform.startswith('win'):
				sys.path.append("c:/oblique/libs/python")
				nuke.pluginAppendPath("C:/oblique/software/Nuke/NukePlugins")
			else:
				sys.path.append("/oblique/libs/python")
				nuke.pluginAppendPath("/oblique/software/Nuke/NukePlugins")
			'''

		if sInFilename != "":
			self.script += '''
			sInFilename = '%s'
			iStartFrame = %d
			iEndFrame = %d
			n = nuke.createNode("Read")
			n.knob('file').setValue(sInFilename)
			n.knob('first').setValue(iStartFrame)
			n.knob('last').setValue(iEndFrame)
			if sInFilename.find("Render_Pictures") != -1:
				n.knob("premultiplied").setValue(True)
			''' % (sInFilename, iStartFrame, iEndFrame)
		else:
			self.script += '''
			iStartFrame = %d
			iEndFrame = %d
			n = nuke.createNode('Constant')
			'''% (iStartFrame, iEndFrame)

		self.script += self._convertKwargs(kwargs)

		self.script += '''
			nuke.root().knob("first_frame").setValue(iStartFrame)
			nuke.root().knob("last_frame").setValue(iEndFrame)
			'''

	def createNode(self, sNodeName, **kwargs):
		'''
		Adds a node in the script. Knobs values can be set via
		keyword arguments.
		example:
			np = createNode('Write', file='C:/patate.####.exr', premultiplied=True)

		Internally, createNode() returns n, and uses n.knob().setValue() to
		set the parameters. If you need to create some branches, you might want
		to use saveNodeInVariable([variable]) to keep the last added node in a safe variable
		since n will always be overwritten on the next createNode(). You can then later use
		connectInput([variable]) to connect the second input of a merge node for example.
		See http://francoislord.com/blog/computer-graphics/nuke/nukeprocess_74 for examples.
		'''
		self.script += "n = nuke.createNode('%s')\n" % sNodeName
		self.script += self._convertKwargs(kwargs)

	def saveNodeInVariable(self, sVariable):
		self.addCode("%s = n" % sVariable)

	def connectInput(self, sVariable):
		self.addCode("n.connectInput(0, %s)" % sVariable)

	def addCode(self, sCode):
		'''
		Adds a line of code to the script.
		'''
		self.script += sCode + "\n"

	def execute(self, iStartFrame = None, iEndFrame = None, iStep = None):
		'''
		Launches the render and returns a subprocess.Popen instance.
		stdios are piped so you can use oProcess.stdin.readline().
		Optional args:
			iStartFrame, iEndFrame, iStep
		'''
		self._endScript(iStartFrame, iEndFrame, iStep)

		#print self.getScript()
		oProcess = subprocess.Popen('%s -t -' % (self._nukeExe), stdin=subprocess.PIPE,
									stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=True, universal_newlines=True)
		oProcess.stdin.write(self.getScript())
		return oProcess

	def executeVerbose(self, iStartFrame = None, iEndFrame = None, iStep = None):
		'''
		Launches the render and prints the output of the process.
		Optional args:
			iStartFrame, iEndFrame, iStep
		'''
		oProcess = self.execute(iStartFrame, iEndFrame, iStep)
		sOutLine = "."
		while sOutLine != "":
			sOutLine = oProcess.stdout.readline()
			print sOutLine
		return oProcess.returncode

	def getScript(self):
		'''
		Returns the script in its ready-to-use form,
		with the right indentation.
		'''
		sCleanedScript = ""
		for sLine in self.script.splitlines(True):
			if sLine.startswith("\t\t\t"):
				sCleanedScript += sLine.replace("\t\t\t", "", 1)
			else:
				sCleanedScript += sLine
		return sCleanedScript

	def _endScript(self, iStartFrame = None, iEndFrame = None, iStep = None):
		'''
		Adds the nuke.executeMultiple() call and sets the
		root.first_frame and root.last_frame variables in case they're
		different from the root script.
		'''
		if not iStartFrame: iStartFrame = "nuke.root().knob('first_frame').value()"
		if not iEndFrame: iEndFrame = "nuke.root().knob('last_frame').value()"
		if not iStep: iStep = "1"
		self.script += '''
			L = nuke.allNodes("Write")
			result = nuke.executeMultiple(L, ((%s, %s, %s),))
			\nquit(not result)\n
			''' % (str(iStartFrame), str(iEndFrame), str(iStep))

	def _convertKwargs(self, dKwargs):
		# Always return 'file' and 'filetype' first because it is needed before we can set any options on it.
		def kwsort(x,y):
			lOrder = ["file", "file_type"]
			if x in lOrder and y in lOrder:
				return cmp(lOrder.index(x), lOrder.index(y))
			elif x in lOrder:
				return -1
			elif y in lOrder:
				return 1
			else:
				return cmp(x, y)

		lKeys = sorted(dKwargs.keys(), kwsort)
		sReturnScript = ""
		for sKey in lKeys:

			if isinstance(dKwargs[sKey], (str,unicode)):
				if dKwargs[sKey] == "False" or dKwargs[sKey] == "True":
					sReturnScript += "n.knob('%s').setValue(%s)\n" % (sKey, dKwargs[sKey])
				elif dKwargs[sKey].startswith('{') and dKwargs[sKey].endswith('}'):
					sReturnScript += "n.knob('%s').setExpression('%s',0)\n" % (sKey, dKwargs[sKey][1:-1])
				else:
					sReturnScript += "n.knob('%s').setValue('%s')\n" % (sKey, dKwargs[sKey])
			elif isinstance(dKwargs[sKey], float):
				sReturnScript += "n.knob('%s').setValue(%f)\n" % (sKey, dKwargs[sKey])
			elif isinstance(dKwargs[sKey], bool):
				sReturnScript += "n.knob('%s').setValue(%s)\n" % (sKey, dKwargs[sKey])
			elif isinstance(dKwargs[sKey], (int, long)):
				sReturnScript += "n.knob('%s').setValue(%d)\n" % (sKey, dKwargs[sKey])
			else:
				raise TypeError, "Unrecognized knob variable type: %s\n%s: %s" % (type(dKwargs[sKey], sKey, str(dKwargs[sKey])))
		return sReturnScript
