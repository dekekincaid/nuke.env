# reportABug.py
# Author: Deke Kincaid, The Foundry
# v1.0
# 10/19/11
#
# python panel for reporting bugs/feature requests to the foundry
#
# 
# Install Instructions:
# 1. copy the file into your .nuke folder or anywhere in your NUKE_PATH 
# 2. in your init.py or menu.py put the following code:
#
#import reportABug
#def addRABPanel():
#    rabPanel = reportABug.reportABug()
#    return rabPanel.addToPane()
#nuke.menu('Pane').addCommand('Report A Bug', addRABPanel, "ctrl+alt+b")
#nukescripts.registerPanel('com.deke.reportABug', addRABPanel)
# 
#
# Any issues then email me or post a reply in the comments on nukepedia
# dekekincaid@gmail.com

import os
import re
import nuke
import nukescripts
import platform
import subprocess
import urllib
import webbrowser

class reportABug( nukescripts.PythonPanel ):
	def __init__( self ):
		nukescripts.PythonPanel.__init__( self, 'Report and Bug', 'com.deke.reportABug')
		
		# CREATE KNOBS
		self.featureRequest = nuke.String_Knob('name', 'Your Name')
		self.featureRequest = nuke.String_Knob('company', 'Company')
		self.featureRequest = nuke.Boolean_Knob('featureRequest', 'Feature Request?')
		self.shortDescription = nuke.Multiline_Eval_String_Knob('shortDescription', 'Short Description(Subject)')
		self.fullDescription = nuke.Multiline_Eval_String_Knob('fullDescription', 'Full Description')
		self.problemNodes = nuke.Multiline_Eval_String_Knob('problemNodes', 'Nodes Selected')
		self.problemNodes.setEnabled( False )
		self.systemInfo = nuke.Multiline_Eval_String_Knob('systemInfo', 'System Info')
		self.systemInfo.setEnabled( False )
		self.line = nuke.Text_Knob('line', '')
		self.update = nuke.PyScript_Knob('update', 'Update')
		self.sendEmail = nuke.PyScript_Knob('sendEmail', 'Send Email to The Foundry')
		self.nukeVersion = nuke.PyScript_Knob('nukeVersion', 'Nuke Version')
		
		self.operatingSystem = nuke.PyScript_Knob('operatingSystem', 'OS')
		self.nukeVersion = nuke.PyScript_Knob('nukeVersion', 'Nuke Version')
		
		self.emailFrom = nuke.String_Knob('emailFrom', 'Your Email Address:')
		self.emailTo = "support@thefoundry.co.uk"
		self.SMTPServer = nuke.String_Knob('SMTPServer', 'SMTP Server:')
		
		# ADD KNOBS
		self.addKnob( self.name )
		self.addKnob( self.company )
		self.addKnob( self.featureRequest )
		self.addKnob( self.shortDescription )
		self.addKnob( self.fullDescription )
		self.addKnob( self.problemNodes )
		self.addKnob( self.systemInfo )
		self.addKnob( self.line )
		self.addKnob( self.update )
		self.update.setFlag( nuke.STARTLINE )
		self.addKnob( self.sendEmail )
		
		self.addKnob( self.emailFrom )
		self.addKnob( self.SMTPServer )

	def __NodeHasKnobWithName( self, node, name):
		try:
			node[name]
		except NameError:
			return False
		return True
	
	def __FindNode( self, searchstr, knob):
		v = knob.value()
		if v and searchstr and searchstr in v:
			return True
	
	def search( self, searchstr, nodes ):
		""" Search in nodes with file knobs. """
		fileKnobNodes = [i for i in nodes if self.__NodeHasKnobWithName(i, 'file')]
		proxyKnobNodes = [i for i in nodes if self.__NodeHasKnobWithName(i, 'proxy')]
		if not fileKnobNodes and not proxyKnobNodes: raise ValueError, "No file nodes selected"
		nodeMatches = []
		knobMatches = []
		for i in fileKnobNodes:
			if self.__FindNode(searchstr, i['file']):
				nodeMatches.append( i )
				knobMatches.append( i['file'] )            
		for i in proxyKnobNodes:
			if self.__FindNode(searchstr, i['proxy']):
				nodeMatches.append( i )
				knobMatches.append( i['proxy'] )
		return nodeMatches, knobMatches		
	
		
	def getSearchResult( self, nodes ):
		nodeMatches, knobMatches = self.search( self.searchStr.value(), nodes )
		nodes = [n.name() for n in nodeMatches]
		infoStr = '%s node(s) found:\n\t%s' % ( len(nodes), ', '.join( nodes ) )
		self.info.setValue( infoStr )
		return knobMatches
		
	def knobChanged( self, knob ):
		if knob in (self.searchStr, self.update, self.nodesChoice):
			srcNodes = { 'all': nuke.allNodes(), 'selected': nuke.selectedNodes() }
			self.matches = self.getSearchResult( srcNodes[self.nodesChoice.value()] )
		elif knob is self.replace and self.matches is not None:
			for k in self.matches:
				newStr = re.sub( self.searchStr.value(), self.replaceStr.value(), k.value() )
				k.setValue( newStr )

#open email application
	def mailto_url(to=None,subject=None,body=None,cc=None):
    	url = "mailto:" + urllib.quote(to.strip(),"@,")
    	sep = "?"
#    	if cc:
#        	url+= sep + "cc=" + urllib.quote(cc,"@,")
#        	sep = "&"
    	if subject:
        	url+= sep + "subject=" + urllib.quote(subject,"")
        	sep = "&"
    	if body:
        	body="\r\n".join(body.splitlines())
        	url+= sep + "body=" + urllib.quote(body,"")
        	sep = "&"
    	return url

	url = mailto_url('email address', 'subject', 'message body')
	webbrowser.open(url,new=1)

#email through python, ie don't open email client
#I took this from nathan's example he posted on vfxtalk
#thanks nathan
	def emailPython
	
		# See if the user has setup a few vars to auto set the default email account info.

		# From email address.
		try:
			nemailFrom
		except NameError:
			pass
		else:
			self.emailFrom = nemailFrom

		# To email address.
		try:
			nemailTo
		except NameError:
			pass
		else:
			self.emailTo = nemailTo

		# STMPServer address.
		try:
			nemailSMTPServer
		except NameError:
			pass
		else:
			self.SMTPServer = nemailSMTPServer
		
		# Email account password.
		try:
			nemailPassword
		except NameError:
			pass
		else:
			self.emailPassword = nemailPassword
		
		# Email subject.
		try:
			nemailSubject
		except NameError:
			pass
		else:
			self.emailSubject = nemailSubject

		# Email message.
		try:
			nemailSubject
		except NameError:
			pass
		else:
			self.emailMessage = nemailMessage

		self.comp_panel = nuke.Panel("Compose email")
		self.comp_panel.addSingleLineInput("From:", self.emailFrom)
		self.comp_panel.addSingleLineInput("To:", self.emailTo)
		self.comp_panel.addSingleLineInput("SMTP Server:", self.SMTPServer)
		self.comp_panel.addSingleLineInput("Password:", self.emailPassword)
		self.comp_panel.addSingleLineInput("Subject:", self.emailSubject)
		self.comp_panel.addMultilineTextInput("Message:", self.emailMessage)
		self.comp_panel.addButton("Cancel")
		self.comp_panel.addButton("Send")

	def compose(self):
		if self.comp_panel.show():
			self.emailFrom = self.comp_panel.value("From:")
			self.emailTo = self.comp_panel.value("To:")
			self.SMTPServer = self.comp_panel.value("SMTP Server:")
			self.emailPassword = self.comp_panel.value("Password:")
			self.emailSubject = self.comp_panel.value("Subject:")
			self.emailMessage = self.comp_panel.value("Message:")

			while self.comp_panel.value("From:").__len__() == 0:
				nuke.message("Email sender is empty.")
				if self.comp_panel.show() == False:
					return False

			while self.comp_panel.value("To:").__len__() == 0:
				nuke.message("Email recipient is empty.")
				if self.comp_panel.show() == False:
					return False

			while self.comp_panel.value("SMTP Server:").__len__() == 0:
				nuke.message("SMTPServer is empty.")
				if self.comp_panel.show() == False:
					return False

			while self.comp_panel.value("Password:").__len__() == 0:
				nuke.message("Email password is empty.")
				if self.comp_panel.show() == False:
					return False

			self.send()

	def send(self):
		emailData = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % \
		(self.emailFrom, self.emailTo, self.emailSubject)) + self.emailMessage

		server = smtplib.SMTP(self.SMTPServer)
		try:
			server.login(self.emailFrom, self.emailPassword)
		except:
			nuke.message("Login error!")
		else:
			try:
				server.sendmail(self.emailFrom, self.emailTo, emailData)
			except:
				nuke.message("Error sending email!")
			else:
				pass

		server.quit()

nuke_email = nuke_email()
# Use the below command to open the compose window and send an email.
# nuke_email.compose()

#list of stuff to print out in the email
nuke.env [“PluginExtension”].
