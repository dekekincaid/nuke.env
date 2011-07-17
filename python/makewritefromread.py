import os
import nuke

#
# "Make Write from Read" v 1.2
#  Written by Hakan Blomdahl



# how to install:
#
# import makewritefromread
#
# # Add extra Tools menu
# mymenubar=nuke.menu("Nuke")
# m=mymenubar.addMenu("Tools")
#
# # Create Tools menu for right click menu:
# nodetoolbar = nuke.menu("Nodes")
# t=nodetoolbar.addMenu("Tools")
#
# m.addCommand("Make Write of Read...", 'makewritefromread.make_write_from_read()', '')
# t.addCommand("Make Write of Read...", 'makewritefromread.make_write_from_read()', '')




def find_upstream_node( matchclass=None, startnode=None ):
	"""
	In the simplest way possible, this function will go upstream and find
	the first node matching the specified class.
	"""

	if matchclass == None:
		return None
	#
	if startnode == None:
		return None
	#
	if  startnode.Class() == matchclass:
		return startnode
	else:
		return find_upstream_node( matchclass=matchclass, startnode=startnode.input( 0 ) )
	#
#

def make_write_from_read():
	"""
	This method will assist automated creation of Write-nodes, using the filename of
	upstream Read-nodes.
	
	Typical scenario:
		1. Drop in a bunch of still images.
		2. Foreach image add some, for example, Grade-nodes and fix a good look.
		3. Now select all grade-nodes and run this script.
		4. The script will look for an upstream Read-node and use that filename
		   for creation of write nodes. The panel that presents itself will allow
		   you to modify that filename or path.
	"""

	if len( nuke.selectedNodes() ) < 1:
		return
	#

	readNodeLut = {}
	# Build Lookup for each selected node.
	for tmpNode in nuke.selectedNodes():
		readNode = find_upstream_node( matchclass="Read", startnode=tmpNode )
		if readNode:
			readNodeLut[tmpNode] = readNode
		#
	#

	#	autocrop true
		
	
	if len( readNodeLut ) < 1:
		return
	#

	
	formatList = []
	formatList.append( "nochange" )
	formatList.append( "jpeg" )
	formatList.append( "tiff" )
	formatList.append( "exr" )
	formatList.append( "dpx" )
	formatList.append( "png" )

	tiffDatatypeList = []
	tiffDatatypeList.append( '"16 bit"' )
	tiffDatatypeList.append( '"8 bit"' )
	tiffDatatypeList.append( '"32 bit float"' )

	tiffCompressionList = []
	tiffCompressionList.append( '"LZW"' )
	tiffCompressionList.append( '"none"' )
	tiffCompressionList.append( '"Deflate"' )
	tiffCompressionList.append( '"PackBits"' )

	exrDatatypeList = []
	exrDatatypeList.append( '"16 bit half"' )
	exrDatatypeList.append( '"32 bit float"' )

	exrCompressionList = []
	exrCompressionList.append( '"PIZ Wavelet (32 scanlines)"' )	# good grainy images
	exrCompressionList.append( '"Zip (1 scanline)"' ) # cg and lots of black
	exrCompressionList.append( '"Zip (16 scanlines)"' ) # cg and lots of black
	exrCompressionList.append( '"RLE"' )
	exrCompressionList.append( '"B44"' )
	exrCompressionList.append( '"none"' )
	
	jpegQualityList = []
	jpegQualityList.append( "1.0" )
	jpegQualityList.append( "0.9" )
	jpegQualityList.append( "0.8" )
	jpegQualityList.append( "0.7" )
	jpegQualityList.append( "0.6" )
	jpegQualityList.append( "0.5" )
	jpegQualityList.append( "0.4" )
	jpegQualityList.append( "0.3" )
	jpegQualityList.append( "0.2" )
	jpegQualityList.append( "0.1" )
	
	formatPulldown = " ".join( formatList )
	jpegQualityPulldown = " ".join( jpegQualityList )
	tiffDatatypePulldown = " ".join( tiffDatatypeList )
	tiffCompressionPulldown = " ".join( tiffCompressionList )
	exrDatatypePulldown = " ".join( exrDatatypeList )
	exrCompressionPulldown = " ".join( exrCompressionList )

	addPrefix = ""
	addPostfix = ""
	addPath = ""

	addPathHandle = "Path add-on (relative or absolute):"
	addPrefixHandle = "Prefix (added in front of the filename):"
	addPostfixHandle = "Suffix (inserted before the extension):"
	formatPulldownHandle = "Format:"
	jpegQualityPulldownHandle = "Jpeg Quality:"
	tiffDatatypePulldownHandle = "TIFF Datatype:"
	tiffCompressionPulldownHandle = "TIFF Compression:"
	exrDatatypePulldownHandle = "EXR Datatype:"
	exrCompressionPulldownHandle = "EXR Compression:"

	p = nuke.Panel("Make Write of Read")

	p.addSingleLineInput(addPathHandle, addPath )
	p.addSingleLineInput(addPrefixHandle, addPrefix )
	p.addSingleLineInput(addPostfixHandle, addPostfix )
	p.addEnumerationPulldown(formatPulldownHandle, formatPulldown )
	p.addEnumerationPulldown(jpegQualityPulldownHandle, jpegQualityPulldown )
	p.addEnumerationPulldown(tiffDatatypePulldownHandle, tiffDatatypePulldown )
	p.addEnumerationPulldown(tiffCompressionPulldownHandle, tiffCompressionPulldown )
	p.addEnumerationPulldown(exrDatatypePulldownHandle, exrDatatypePulldown )
	p.addEnumerationPulldown(exrCompressionPulldownHandle, exrCompressionPulldown )

	p.addButton("Cancel")
	p.addButton("OK")
	result = p.show()

	#if ok is clicked, panel will return 1 otherwise 0
	if result: 
		pass
	else:
		return None
	#

	# Get Values from enumeration objects.
	selectedFormat = p.value(formatPulldownHandle)
	selectedJpegQuality = p.value(jpegQualityPulldownHandle)
	selectedTiffDatatype = p.value(tiffDatatypePulldownHandle)
	selectedTiffCompression = p.value(tiffCompressionPulldownHandle)
	selectedExrDatatype = p.value(exrDatatypePulldownHandle)
	selectedExrCompression = p.value(exrCompressionPulldownHandle)


	addPath = p.value(addPathHandle)
	addPrefix = p.value(addPrefixHandle)
	addPostfix = p.value(addPostfixHandle)

	if ( addPath == "" ) and ( addPrefix == "" ) and ( addPostfix == "" ):

		if selectedFormat == "nochange":
			result = nuke.ask( "Warning, your write nodes will have the same filename as\nyour Read-nodes.\n\n Are you sure that this is what you want?" )
		else:
			result = nuke.ask( "Warning, you only changed the file format.\n\nYour write nodes MIGHT have the same filename as\nyour Read-nodes.\n\n Are you sure that this is what you want?" )
		#
		if result: 
			pass
		else:
			return None #your script will exit now
		#
	#
	
	# Deselect all
	for tmpNode in nuke.selectedNodes():
		tmpNode['selected'].setValue(False)

	selectThese = []
	for ( tmpNode, readNode ) in readNodeLut.iteritems():
		tmpNode['selected'].setValue(True)

		#originalFilename = readNode["file"]
		originalFilename = nuke.filename( readNode )

		( basepath, filename ) = os.path.split( originalFilename )
		( basefile, extension ) = os.path.splitext( filename )

		if selectedFormat == "nochange":
			tmpExt = extension.lstrip( '.' )
			if ( tmpExt.lower() == "jpg" ) or ( tmpExt.lower() == "jpeg" ):
				type = "jpeg"
			elif ( tmpExt.lower() == "tif" ) or ( tmpExt.lower() == "tiff" ) or ( tmpExt.lower() == "tif16" ):
				type = "tiff"
			else:
				type = tmpExt
			#
		#
		else:
			type = selectedFormat
			extension = "." + type
			if extension == ".jpeg":
				type = "jpeg"
				extension = ".jpg"
			elif extension == ".tiff":
				type = "tiff"
				extension = ".tif"
			#
		#

		normalizedBasepath = os.path.normpath( basepath )
		normalizedAddPath = os.path.normpath( addPath )
		
		#print "normalizedBasepath", normalizedBasepath
		#print "normalizedAddPath", normalizedAddPath
		
		
		# This will also take care of absolute paths.
		newFilename = os.path.join( normalizedBasepath, normalizedAddPath )

		# Remove any ".." and similar.
		newFilename = os.path.normpath( newFilename )

		newFilename = os.path.join( newFilename, addPrefix + basefile + addPostfix + extension ).replace( "\\", "/" )
		
		wn = nuke.createNode("Write", "", inpanel = False )
		wn['selected'].setValue(False)
		wn['file'].setValue( newFilename )
		wn['file_type'].setValue( type )
		if type == "jpeg":
			wn['_jpeg_quality'].setValue( float( selectedJpegQuality ) )
		elif type == "tiff":
			wn['datatype'].setValue( selectedTiffDatatype )
			wn['compression'].setValue( selectedTiffCompression )
		elif type == "exr":
			wn['datatype'].setValue( selectedExrDatatype )
			wn['compression'].setValue( selectedExrCompression )
		#

		wn.setInput( 0, tmpNode )
		selectThese.append( wn )
	#

	for tmpNode in selectThese:
		tmpNode['selected'].setValue( True )
	#
#
