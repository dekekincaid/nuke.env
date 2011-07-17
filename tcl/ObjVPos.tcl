#############
#written by Frank Rueter
# last modified April-22-2006
#	returns all vertex positions in an obj file
# last modified August-19-2007
#	now returns either the vertex positions or the center coordinates of each face (obj faces need to be triangles not polygons!)
#	valid arguments:
#			"f" to get face centers
#			"l" for a list of coordinates where index 0 is the face center and index 1 is a list of the corner coordinates
#			"v" or none to get vertices
############
proc ObjVPos {obj_file args} {
	if {$args != "f" && $args != "v" && $args != "l" && $args != ""} {
		set errormsg "usage:\tObjVPos <obj file> ?mode?\n\n\
			mode:\n\t f - retrieve face centers\n\
			\t l - retrieve list of vertex positions and face centers.\n\
			\t v - retrieve vertex positions.\n\
			\nIf no mode is given vertex positions are returned."
		alert $errormsg
		return
		}
#################################### SUB PROCS ####################################
	proc getFaces {verts faces mode} {
		set facePositions {}
		set faceInfo {};# this will hold the face center as index 0 followed by a list of corner positions as index 2 per face
		foreach curFace $faces {
			set corners {}
			set positionList {}
			foreach curVert $curFace {
				lappend positionList [lindex $verts [expr $curVert-1]]
				}
			set xPos 0
			set yPos 0
			set zPos 0
			foreach curPos $positionList {
				lappend corners $curPos
				set xPos [expr $xPos+[lindex $curPos 0]]
				set yPos [expr $yPos+[lindex $curPos 1]]
				set zPos [expr $zPos+[lindex $curPos 2]]
				}
			set faceX [expr $xPos/[llength $positionList]]
			set faceY [expr $yPos/[llength $positionList]]
			set faceZ [expr $zPos/[llength $positionList]]
			
			lappend facePositions [list $faceX $faceY $faceZ]
			lappend faceInfo [list [list $faceX $faceY $faceZ] $corners]
			}
#puts "####\n$faceInfo\n####"
		switch $mode {
			"center" {return $facePositions}
			"coords" {return $faceInfo}
			}
		}
#################################### SUB PROCS END ####################################		
	set chan [open $obj_file r]
#	puts "\t$obj_file"
	while {[gets $chan line] >= 0} {
		if [regexp {^v\s(.+\s+.+\s+.+)} $line junk coords] {
			lappend obj_verts $coords
			}
		if [regexp {^f\s(.+((\s+)*)+)} $line junk coords] {
			set cleanCoords ""
			foreach curCoord $coords {
				# extracting vertex number from face description (obj face elements read v/vt/vn)
				lappend cleanCoords [lindex [file split $curCoord] 0]
				}
			lappend obj_faces $cleanCoords
			#puts "reading coordinates $cleanCoords ..."
			}
		}
	close $chan
	
	switch $args {
		"v" - "" {return $obj_verts}
		"f" {getFaces $obj_verts $obj_faces center}
		"l" {getFaces $obj_verts $obj_faces coords}
		}
		
	
}
