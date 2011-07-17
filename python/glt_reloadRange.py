# Nuke frame range fixer
# Select read nodes and run the script. It will find the starting and ending frame in the sequence (if exist), and set the frame range to it. 
# (It skips other type of nodes, so you may select other types too)
# Works only if counter is before the extension, and preceded by a . (point)
# Example:
# .../AX1_020_001-cg_fx_v008_cow_beauty.0108.iff
# Useful for example if a 3d rendered sequence is loaded in nuke before the render has ended. 
# Comments are welcome
# by Gabor L. Toth (gltoth@gmail.com)

# version 1.05  2009-11-10	- fixed sorting for linux
# version 1.00  2009-10-21	- cleaned up version
# version 0.12  2009-10-16	- skipping not existing directories
# version 0.11  2009-09-10	- works properly with multiple sequences in the same folder. Handles pattern other than %04d too.
# version 0.10  2009-09-09	- initial version 

import nuke
import os
import os.path
import math
import glob
import re

def  glt_reloadRange():
	sn = [n for n in nuke.selectedNodes() if n.Class() == "Read"]
    
	if sn != []:
		for n in sn:
			seqPath = n.knob('file').value()							#'AUH_010_001-cg_li_v002_H1BodyRL.beauty.%04d.iff'
			if seqPath is not None and re.match('.*\.%0.*', seqPath):
				indx = seqPath.find('%0')								   	# getting padding format
				pattern = '%0' + seqPath[indx + 2] + 'd'
				seqPathMask = seqPath.replace(pattern, '*')	# replacing %04d	'AUH_010_001-cg_li_v002_H1BodyRL.beauty.*.iff'
				print ''
				print 'PathMask: %s' % (seqPathMask)
				seqDir = os.path.dirname(seqPath)
				print 'Directory: %s' % (seqDir)
				if os.path.exists(seqDir):
					files = os.listdir(seqDir)
					#print files
					
			#sorting files
					filteredFiles = glob.glob(seqPathMask)
					filteredFiles.sort()
					if len(filteredFiles) != 0:
						(firstFileName, ext) = os.path.splitext(filteredFiles[0])
						firstFileTags =  firstFileName.split('.')
						
						sfs = firstFileTags[-1]
						print 'Extension: ' + ext 
						sf = int (sfs)    # converted to int
						print "Start frame: %s" % (sf)
						
						(lastFileName, ext) = os.path.splitext(filteredFiles[len(filteredFiles)-1])
						lastFileTags =  lastFileName.split('.')
						efs = lastFileTags[-1]	
						ef = int (efs)
						print "End frame: %s" % (ef)

						n.knob('first').setValue(sf)
						n.knob('last').setValue(ef)
					else:
						print 'No matching files in this directory! Skipping...'
				else:
					print 'Warning! Directory doesnt exist: ' + seqDir 
			else:
				pass
	else:
		pass 
