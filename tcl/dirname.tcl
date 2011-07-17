#
# Copyright (c) 2004 Digital Domain Inc.  All Rights Reserved.
#

# extract the directory from a full path (aka, strip out the image info)
proc dirname {inputpath} {

	regsub \/[    ]*$ $inputpath {} inputpath
	set inputpath [split $inputpath /]
	set inputpath [join [lrange $inputpath 0 [expr [llength $inputpath]-2]] /]
	return $inputpath

}