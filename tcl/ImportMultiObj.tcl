####################################
# written by frank rueter
# import every object contained in a single obj file into multiple ReadGeo nodes
# only works for objs that contain absolute (continuous) vertex numbers
#
# last modified: September/05/2006
# last modified: September/06/2006
#	-fixed bug where input files with more than one "." in the filename wouldn't produce correct output names
#
####################################
proc ImportMultiObj {args} {
	#get input file
	if [catch {set fileIn [get_filename "multi obj" "*.{obj|OBJ}" ]}] {return}
	if ![file exists $fileIn] {error "file not found:\n$filename"}
	set input_chan [open $fileIn r]
	set inName [lindex [split [file rootname $fileIn] "/"] end]
	set subName "subObj"
	set subLocation "[file dirname $fileIn]/"
	set useGroup 1
	#get a few more details if proc is started without arguments
	if {$args == ""} {
		if [catch {panel -w500 "Import objects contained in \"[basename $fileIn]\"" {
			{"Prefix: " subName}
			{"Location: " subLocation f}
			{"Group resulting nodes" useGroup b}
			}		
			}] {return}
		}
	
	if {[file type $subLocation] != "directory"} {set subLocation "[file dirname $subLocation]/"}
	set subGeos {}
	set vertexIndex 0
	set textureVertexIndex 0
	set ObjCounter 0
	set VData ""
	set FData ""
	
	while {![eof $input_chan]} {
		gets $input_chan line
		#collect all data except polygons (lines starting with 'f')
		if ![regexp {^f\s+} $line] {
			if {[regexp {^v\s+} $line] && $ObjCounter > 0} {incr vertexIndex}
			if {[regexp {^vt\s+} $line] && $ObjCounter > 0} {incr textureVertexIndex}
			append VData "$line\n"
			} else {
			#get polygon and smoothing group info
			while {[regexp {^f\s+} $line] || [regexp {^s\s+} $line] && ![eof $input_chan]} {
				set newLine {}
				if {$ObjCounter > 0} {
					#for subsequent sub objects amend polygon information
					if [regexp {^s\s+} $line] {
						#keep smoothing group info as is
						append FData "$line\n"
						} else {
						foreach curVal [lreplace $line 0 0] {
							if [regexp {/+} $curVal del] {
								#amend vertex information for textured objs
								set oldVVal [lindex [split $curVal $del] 0]
								set oldTVal [lindex [split $curVal $del] end]
								set newVVal [incr oldVVal "-$vertexIndex"]
								set newTVal [incr oldTVal "-$textureVertexIndex"]
								lappend newLine "$newVVal$del$newTVal"
								} else {
								#amend vertex information for untextured objs
								lappend newLine [incr curVal "-$vertexIndex"]
								}
							}
							append FData "f $newLine\n"
						}
					} else {
						#for first sub object leave line as is
						append FData "$line\n"
						}
				gets $input_chan line
				}
			#write out sub object
			set outputFile "$subLocation$subName\_$ObjCounter\_$inName.obj"
			set output_chan [open $outputFile w]
			lappend subGeos $outputFile
			puts $output_chan "$VData\n$FData"
			close $output_chan
			#message "writing into\nObject $ObjCounter\n\n$VData\n$FData"
			set VData ""
			set FData ""
			incr ObjCounter
			}
	}
	close $input_chan
	#create ReadGeo node for each sub geo found in input obj
	if $useGroup {
		Group {}
		set parentGroup [stack 0]
		knob $parentGroup.label "multi objs from:\n$fileIn"
		} else {
		set parentGroup root	
		}
	
	in $parentGroup {
		Scene {}
		set MasterScene [stack 0]
		knob $MasterScene.label "$fileIn"
		if $useGroup {
			Output {}
			}
		lappend NewNodes $MasterScene
		set counter 0
		set In [stack 0]
		foreach curGeo $subGeos {
			puts "creating GeoReader for $curGeo..."
			push 0
			ReadGeo {}
			set CurNode [stack 0]
			knob $CurNode.file $curGeo
			knob $CurNode.label "sub obj of\n$fileIn"
			#connect to scene node
			input $MasterScene $counter $CurNode
			incr counter
			lappend NewNodes $CurNode
			}
	}
}