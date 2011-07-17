#############
#written by Frank Rueter
# last modified April-22-2006
#
#returns all vertex positions in an obj file
############
proc ObjVPos {obj_file} {
	set chan [open $obj_file r]
	while {[gets $chan line] >= 0} {
		if [regexp {^v\s(.+\s+.+\s+.+)} $line junk coords] {
			lappend vertices $coords
			}
		}
	close $chan
	return $vertices
}
