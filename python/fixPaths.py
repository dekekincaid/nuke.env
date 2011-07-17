# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# 
# Example that attempts to fix all the missing read paths in a nuke script.
#
# Works on Read, ReadGeo, or Axis nodes.  Doesn't work on proxy paths.

import os, nuke

def getFrame( filename, frame ):
  ffile = filename
  if ffile.find ( "%" ) != -1:
    ffile = ffile %1
  return getFile( ffile )

def getFile( filename ):
  if filename.find ( "%" ) != -1 and filename.find( " " ) != -1:
    filename  = filename [:filename .rfind(' ')]
  return filename

def getCommonBase( str1, str2 ):
  str1reversed = str1[::-1]
  str2reversed = str2[::-1]
  
  commonBit = os.path.commonprefix( [str1reversed, str2reversed] )
  commonBit = commonBit[::-1]
  baseStr1 = str1[ 0 : str1.find ( commonBit ) ]
  baseStr2 = str2[ 0 : str2.find ( commonBit ) ]
  return [baseStr1, baseStr2]

def fixPaths( ):
  oldDir = ""
  newDir = ""
  scriptDir =  os.path.dirname ( nuke.root().knob("name").getValue() )

  for n in nuke.allNodes():
     #### check node types, supports Read, ReadGeo, or Axis nodes. You may want to add more here..
     if n.Class() == "Read" or n.Class() == "ReadGeo" or n.Class() == "ReadGeo2" or n.Class() == "Axis2":
       f = n.knob( "file" )
       filename =  f.getValue()
       print 'Filename is ' + filename
       if filename and filename != '':
         basename = os.path.basename( filename )
         frame = getFrame( filename, nuke.frame() )
         print "Looking for : " + frame
         if not os.path.exists( frame ):
           filename = filename.replace( oldDir, newDir )
           frame = getFrame( filename, nuke.frame() ) 
           print "Looking for new filename " + frame
           if not os.path.exists( frame ):
  
             n = nuke.getClipname( "Looking for " + filename, basename, scriptDir )
             if n != None:
               (oldDir, newDir) = getCommonBase( os.path.dirname( filename ), os.path.dirname( n ) )
               f.setValue ( getFile(n) )
             else:
               pass
           else:
             f.setValue( getFile(filename) )
  
