
#
# Copyright (c) 2003 Digital Domain, Inc.  All Rights Reserved.
#
#amended by Frank Rueter to use Shake syntax:
#	comma delimits single frames
#	dash delimits first and end frame of a range
#	'x' sets increment for range

proc execute_panel {list} {
	set a [knob root.first_frame]
	set b [knob root.last_frame]

	set range $a-$b
	if [catch {set r [get_input "Frames to execute @b;(Shake Syntax):" $range]}] return
	
	set range [rangeToListSimple $r]
	eval [concat execute $list [list $range]]
	}
