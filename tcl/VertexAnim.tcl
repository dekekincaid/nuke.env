#create cards or axes at a given vertex (static or animated) based on obj files
#vertex: requested vertex number (integer)
#object: card or axis
#mode: mode static(0) or animated (1)
proc VertexAnim {vertex object mode} {
	puts "$vertex $object $mode"
	#CREATE NODE(S)
	switch $object {
		"Card" {
			Card -New
			TransformGeo {}
			}
		"Axis" {
			Axis -New
			}
		}
	set newNode [stack 0]
	#STATIC OR ANIMATED?
	if !$mode {
		set vPos [lindex [ObjVPos [value this.file]] $vertex]
		if {$vPos == ""} {alert "no vertex with number [value this.vNum] found"; return}
		knob $newNode.translate $vPos
		} else {
			for {set curFrame [value root.first_frame]} {$curFrame <= [value root.last_frame]} {incr curFrame} {
				puts "reading animation on frame $curFrame:"
				set ObjFile [knob this.file]
				#detour - I shouldn't have to do this but the frame command to step through time seems unreliable
				regexp {.+(%\d+d)\.\w+$} $ObjFile garbage delimiter
				regsub $delimiter $ObjFile [format $delimiter $curFrame] curFile
				###end of detour
				if ![file exists $curFile] {alert "File Not Found:\n$curFile\n\naborting..."; return}
				set vPos [lindex [ObjVPos $curFile] $vertex]
				puts "\t$vPos"
				setkey $newNode.translate.x $curFrame [lindex $vPos 0]
				setkey $newNode.translate.y $curFrame [lindex $vPos 1]
				setkey $newNode.translate.z $curFrame [lindex $vPos 2]								
				}
			return "DONE"
			}
	}

