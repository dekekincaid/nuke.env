from xml.etree import ElementTree
import nuke
import nukescripts
import os
import re

class SearchReplacePanel( nukescripts.PythonPanel ):
    def __init__( self, historyFile='~/.nuke/srhistory.xml', maxSteps=10 ):
        '''
        Search and Replace panel
        args:
           historyFile  -  file to manage recent search&replace actions
           maxSteps  -  amount of steps to keep in history file
        '''
        nukescripts.PythonPanel.__init__( self, 'Search and Replace', 'com.ohufx.SearchReplace')

        # VARS
        self.historyFile = os.path.expandvars( os.path.expanduser( historyFile ) )
        self.maxSteps = maxSteps
        self.delimiter = ' |>>| '
        # CREATE KNOBS
        self.nodesChoice = nuke.Enumeration_Knob( 'nodes', 'Source Nodes', ['all', 'selected'])
        self.nodesChoice.setTooltip( 'Chose to perform action on all nodes with file knobs or only selected ones' )
        self.history = nuke.Enumeration_Knob( 'history', 'Recent Searches', self.loadHistory() )
        self.history.setTooltip( 'Use the history to quicky access previous search&replace actions.\n By default the history file is stored as "~/.nuke/srhistory.xml" but this can be changed via the "historyFile" argument when creating the panel object. It is also possible to change the size of the history via the "maxSteps" argument to the panel object. Default is 10' )
        self.case = nuke.Boolean_Knob( 'case', 'case sensitive' )
        self.case.setFlag( nuke.STARTLINE )
        self.case.setValue( True )
        self.case.setTooltip( 'Set whether or not the search should be case sensitive' )
        self.searchStr = nuke.String_Knob('searchStr', 'Search for:')
        self.searchStr.setTooltip( 'The text to search for' )
        self.update = nuke.PyScript_Knob('update', 'Update')
        self.update.setTooltip( 'update the search result and preview. This is automaticaly performed and usually should only be required when the node selection has canged' )
        self.replaceStr = nuke.String_Knob('replaceStr', 'Replace with:')
        self.replaceStr.setTooltip( 'Text to replace the found text with' )
        self.replace = nuke.PyScript_Knob('replace', 'Replace')
        self.replace.setTooltip( 'Perform replace action. The preview will update afterwards and the action is added to the history' )
        self.info = nuke.Multiline_Eval_String_Knob('info', 'Found')
        self.info.setEnabled( False )
        self.info.setTooltip( 'See the search results and a preview of the replace action before it is performed' )
        # ADD KNOBS
        for k in ( self.nodesChoice, self.history, self.case, self.searchStr, self.update, self.replaceStr, self.replace, self.info):
            self.addKnob( k )
        self.matches = None

    def loadHistory( self ):
        '''load history file to update knob'''
        print 'loading search&replace history'
        # GET EXISTING HISTORY
        if not os.path.isfile( self.historyFile ):
            return []
        # READ EXISTING FILE
        xmlTree = ElementTree.parse( self.historyFile )
        itemList = ['%s%s%s' % ( n.attrib['search'], self.delimiter, n.attrib['replace'] ) for n in xmlTree.findall( 'ITEM' )][-self.maxSteps:]
        itemList.reverse()
        itemList.insert( 0, '-- select --' )
        return itemList
    
    def updateHistory( self, sString, rString ):
        '''
        updates history file
        args:
           sString  -  search string to add to history
           rString  -  replace string to add to history
        TODO  -  IMPLEMENT MAX VALUE
        '''
        itemList = []
        # READ EXISTING FILE
        if os.path.isfile( self.historyFile ):
            xmlTree = ElementTree.parse( self.historyFile )
            for n in xmlTree.findall( 'ITEM' ):
                attr = n.attrib
                itemList.append( attr )
       
        # IGNORE ATTRIBUTES THAT ARE ALREADY IN HISTORY
        entryExists = False
        for i in itemList:
            if i['search'] == sString and i['replace']==rString:
                entryExists = True
                break

        # IF ATTRIBUTES DONT EXIST IN HISTORY, ADD THEM
        if not entryExists:
            # PREP DICTIONARY FOR XML DUMP
            srItem = dict(search=sString, replace=rString )
            itemList.append( srItem )
            # BUILD XML TREE
            root = ElementTree.Element( 'SearchReplacePanel')
            for i in itemList[-self.maxSteps:]:
                ElementTree.SubElement( root, 'ITEM', attrib=i )
            tree = ElementTree.ElementTree( root )
            # DUMP XML TREE
            print 'WRITING TO:', self.historyFile
            tree.write( self.historyFile )

    def search( self, searchstr, nodes ):
        """ Search in nodes with file knobs. """
        fileKnobNodes = [i for i in nodes if self.__NodeHasKnobWithName(i, 'file')]
        proxyKnobNodes = [i for i in nodes if self.__NodeHasKnobWithName(i, 'proxy')]
        if not fileKnobNodes and not proxyKnobNodes: raise ValueError, "No file nodes selected"
        nodeMatches = []
        knobMatches = []
        for i in fileKnobNodes:
            if self.__findNode(searchstr, i['file'] ):
                nodeMatches.append( i )
                knobMatches.append( i['file'] )            
        for i in proxyKnobNodes:
            if self.__findNode(searchstr, i['proxy'] ):
                nodeMatches.append( i )
                knobMatches.append( i['proxy'] )
        return nodeMatches, knobMatches        
        
    def getSearchResults( self, nodes ):
        # PERFORM SEARCH AND UPDATE INFO KNOB
        nodeMatches, knobMatches = self.search( self.searchStr.value(), nodes )
        nodes = [n.name() for n in nodeMatches]
        infoStr1 = '%s node(s) found:\n\t%s' % ( len(nodes), ', '.join( nodes ) )
        infoStr2 = ''
        for k in knobMatches:
            newStr = nukescripts.replaceHashes( self.__doReplace( k ) )
            # CHECK IF PATH IS VALID FOR CURRENT FRAME
            curFrame = int( nuke.Root()['frame'].value() ) # there is a bug which prevents nuke.frame() to work properly inside of python panels (6.3v5)
            try:
                curPath = newStr % curFrame
            except:
                curPath = newStr
            exists = {True:'  VALID PATH AT FRAME %s' % curFrame, False:'  !!! PATH IS INVALID AT CURRENT FRAME (%s)!!!' % curFrame}[os.path.exists( curPath )]
            # BUILD INFO STRING
            infoStr2 += '%s.%s:\n\tbefore\t%s\n\tafter\t%s  %s\n' % ( k.node().name(), k.name(), k.value(), newStr, exists )
        self.info.setValue( '\n'.join( [infoStr1, infoStr2] ) )
        return knobMatches

    def __NodeHasKnobWithName( self, node, name):
        try:
            node[name]
        except NameError:
            return False
        return True
    
    def __findNode( self, searchstr, knob ):
        v = knob.value()
        if not self.case.value():
            v = v.lower()
            searchstr = searchstr.lower()
        if v and searchstr and searchstr in v:
            return True    
    
    def __doSearch( self ):
        # LAUNCH SEARCH
        srcNodes = { 'all': nuke.allNodes(), 'selected': nuke.selectedNodes() }
        self.matches = self.getSearchResults( srcNodes[self.nodesChoice.value()] )

    def __doReplace( self, knob ):
        # PERFORM REPLACE
        if self.case.value():
            # CASE SENSITIVE
            newStr = re.sub( self.searchStr.value(), self.replaceStr.value(), knob.value() )
        else:
            # IGNORE CASE
            newStr = knob.value()
            for m in re.findall( self.searchStr.value(), knob.value(), re.IGNORECASE ):
                newStr = re.sub( m, self.replaceStr.value(), newStr )

        return newStr

    def knobChanged( self, knob ):
        if knob in ( self.searchStr, self.replaceStr, self.update, self.nodesChoice, self.case ):
            # PERFORM SEARCH
            self.__doSearch()
        elif knob is self.replace and self.matches is not None:
            # PERFORM REPLACE AND UPDATE HISTORY
            print 'replacing'
            for k in self.matches:
                k.setValue( self.__doReplace( k ) )

            self.updateHistory( self.searchStr.value(), self.replaceStr.value() )
            self.history.setValues( self.loadHistory() )
            self.history.setValue( 0 )
            self.__doSearch()
        elif knob is self.history:
            search, replace = knob.value().split( self.delimiter )
            self.searchStr.setValue( search )
            self.replaceStr.setValue( replace )
            self.__doSearch()