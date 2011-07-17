proc compressList2 {fileList} {
	array set frameInfo {}
	set compressedStuff {}
	set singleFiles {}
	foreach cur_file $fileList {
		set cur_file [string trim $cur_file "\""]
		#find files with digits that could be frame numbers
		if [info exists frameNumber] {unset frameNumber}
		regexp {(.+)(\D+)(\d+)(\.\w+)$} $cur_file garbage baseName delimiter frameNumber suffix
		if ![info exists frameNumber] {
			#collect files without numbers
			lappend singleFiles "\"$cur_file\""
			} else {
			#collect files with numbers and format them
			set formatString [format %02d [string length $frameNumber]]
			lappend frameInfo($baseName$delimiter%$formatString\d$suffix) $frameNumber
			}
		}
	foreach curSeq [array names frameInfo] {
		#step through compressed sequences
		#get first and last frame and get rid of leading zeros
		scan [lindex [lsort $frameInfo($curSeq)] 0] "%d" firstFrame
		scan [lindex [lsort $frameInfo($curSeq)] end] "%d" lastFrame		
		if {$firstFrame == $lastFrame} {
			#collect single files with numbers (i.e. single frames) and undo the formatting
			lappend singleFiles "\"[format $curSeq $firstFrame]\""
			} else {
				#collect compressed sequences
				lappend compressedStuff [list $curSeq $firstFrame-$lastFrame]
				}
		}
	return [concat $singleFiles $compressedStuff]
	}