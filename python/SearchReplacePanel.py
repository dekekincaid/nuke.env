import nuke
import nukescripts
import re

class SearchReplacePanel( nukescripts.PythonPanel ):
	def __init__( self ):
		nukescripts.PythonPanel.__init__( self, 'Search and Replace', 'com.ohufx.SearchReplace')
		# CREATE KNOBS
		self.nodesChoice = nuke.Enumeration_Knob( 'nodes', 'Source Nodes', ['all', 'selected'])
		self.searchStr = nuke.String_Knob('searchStr', 'Search for:')
		self.update = nuke.PyScript_Knob('update', 'Update')
		self.info = nuke.Multiline_Eval_String_Knob('info', 'Found')
		self.info.setEnabled( False )
		self.replaceStr = nuke.String_Knob('replaceStr', 'Replace with:')
		self.replace = nuke.PyScript_Knob('replace', 'Replace')
		# ADD KNOBS
		self.addKnob( self.nodesChoice )
		self.addKnob( self.searchStr )
		self.addKnob( self.update )
		self.addKnob( self.info )
		self.addKnob( self.replaceStr )
		self.addKnob( self.replace )
		
		self.matches = None

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

