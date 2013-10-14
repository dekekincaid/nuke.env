#add a network location for gizmos and stuff
#nuke.pluginAddPath('Z://1_jobs//_JobTools//scripts//nuke_gizmos')

#windows environment
#nuke.pluginAddPath(os.path.expanduser("~//My Documents//nukescripts"))
#nuke.pluginAddPath(os.path.expanduser("~//My Documents//nukescripts//plugins"))
#nuke.pluginAddPath(os.path.expanduser("~//My Documents//nukescripts//python"))
#nuke.pluginAddPath(os.path.expanduser("~//My Documents//nukescripts//tcl"))
#nuke.pluginAddPath(os.path.expanduser("~//My Documents//nukescripts//gizmos"))
#nuke.pluginAddPath(os.path.expanduser("~//My Documents//nukescripts//icons"))

#linux osx environment

if os.name == "nt":
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//config"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//gizmos"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//gizmos.private"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//gizmos.unused"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//icons"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//lut"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//lut.private"))
	nuke.pluginAddPath("C://Program Files//Mari2.0v1//Bundle//Media//Scripts//Nuke")
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//plugins"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//python"))
	nuke.pluginAddPath(os.path.expanduser("~//Dropbox//nukescripts//tcl"))
else:
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/config"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/gizmos"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/gizmos.private"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/gizmos.unused"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/icons"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/lut"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/lut.private"))
#	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/mari"))
#nuke.pluginAddPath(os.path.expanduser("~/nukescripts/ocio")) #for custom ocio install, don't need it now that it is included with 6.3v7
	nuke.pluginAddPath("/usr/local/Mari2.0v1/Media/Scripts/Nuke")
	nuke.pluginAddPath("/Applications/Mari2.5v1b7/Contents/Media/Scripts/Nuke")
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/plugins"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/python"))
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/stereoNukeToolkit"))
	
	nuke.pluginAddPath(os.path.expanduser("~/nukescripts/tcl"))



def createWriteDir(): 
    import nuke, os 
    file = nuke.filename(nuke.thisNode()) 
    dir = os.path.dirname( file ) 
    osdir = nuke.callbacks.filenameFilter( dir ) 
    try: 
        os.makedirs( osdir ) 
        return 
    except: 
        return 
 
nuke.addBeforeRender( createWriteDir )


#nuke.pluginAddPath("/usr/local/lib") #for custom ocio install, don't need it now that it is included with 6.3v7


#nuke.pluginAddPath(os.path.expanduser("~/nukescripts/other"))
#nuke.pluginAddPath(os.path.expanduser("~/nukescripts/flipbook"))


#nuke.pluginAddPath("/Applications/Pixar/RenderMan.app/Versions/RenderManProServer-15.2/lib")
#nuke.pluginAddPath(os.path.expanduser("~/nukescripts/QATools"))

#nuke.ViewerProcess.register("Cineon", nuke.createNode, ("ViewerProcess_1DLUT", "current Cineon"))
#nuke.pluginAddPath(os.path.expanduser("~/nkLIBRARY/LIBRARY"))

#ocio version control

#setup stereo views automatically


import nodeOps#I need this to render for some reason, will figure out why later

#creates directory when you render to one which doesn't exist
#def createWriteDir():
#	import nuke, os
#	file = nuke.filename(nuke.thisNode())
#	dir = os.path.dirname( file )
#	osdir = nuke.callbacks.filenameFilter( dir )
#	os.makedirs( osdir )
#nuke.addBeforeRender(createWriteDir)
