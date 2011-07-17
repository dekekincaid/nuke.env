#written by frank rueter frank@beingfrank.info
#
#last modified:
#		Jan 16th 2007	- fixed compatibility with 4.5.27
#				- reads the frame padding properly now
#				- checks if files exist on disk and pops up warning message if they don't
#		Jan 17th 2007	- if nothing is selected normal Read nodes are created again
#		Mar 21st 2007	- if nodes are selected which aren't Write nodes a single Read node is creaded
#		Apr 18th 2007	- fixed glob command that caused dots showing up in proxy path
#		Jul 31th 2007	- added support for the create_read proc that comes with Nuke4.7 and later

proc compressList {fileList} {
	array set frameInfo {}
	set compressedStuff {}
	set singleFiles {}
	foreach cur_file $fileList {
		#find files with digits that could be frame numbers
		if [info exists frameNumber] {unset frameNumber}
		regexp {(.+)(\D+)(\d+)(\.\w+)$} $cur_file garbage baseName delimiter frameNumber suffix
		if ![info exists frameNumber] {
			#collect files without numbers
			lappend singleFiles $cur_file
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
			lappend singleFiles [format $curSeq $firstFrame]
			} else {
				#collect compressed sequences
				lappend compressedStuff "$curSeq $firstFrame-$lastFrame"
				}
		}
	return [concat $singleFiles $compressedStuff]
	}

proc missingFiles {filename first last} {
	for {set cur_frame $first} {$cur_frame <= $last} {incr cur_frame} {
		set curFile [format $filename $cur_frame]
		if ![file exists $curFile] {lappend missingFiles $curFile}
		}
	if [info exists missingFiles] {
		return $missingFile
		} else {
			return 0
			}
	}


proc SmartRead {} {
	proc defRead {} {
	global nuke_version
		#do the default thing if nothing is selected
			if {$nuke_version <5} {
				if [catch {create_read}] {Read;return}
				} else {
				python nukescripts.create_read()
				}
		}

	if [catch {selected_nodes}]  {defRead;return}

	foreach cur_node [selected_nodes] {
		puts "cur node is: [class $cur_node]"
		if {[lsearch {Write J2Write WriteProxy_JOE Write_WProxy_47} [class $cur_node]] < 0} {continue}
		puts "\t[value $cur_node.name]"
		set fileKnob [knob $cur_node.file]
		set proxyKnob [knob $cur_node.proxy]
		catch {unset quantifier}
		if ![regexp {%(\d+)d} $fileKnob quantifier pad] {regexp {%(\d+)d} $proxyKnob quantifier pad}


		#SEQUENCE

		if [info exists quantifier] {
			#COLLECT ALL EXISTING FILES THAT MATCH PATTERN
			set mask [string repeat "?" $pad]
			set allFiles [lsort [glob -nocomplain -types f [regsub $quantifier $fileKnob $mask]]]
			set allProxies [lsort [glob -nocomplain -types f [regsub $quantifier $proxyKnob $mask]]]

			#COMPRESS FILES INTO LIST
			set filelist [compressList $allFiles]
			set proxylist [compressList $allProxies]

			#IF NO FRAMES EXIST ON DISK
			# BASE FILE
			if {$fileKnob != ""} {
				puts "checking base file.."
				if {[llength $filelist] == 0} {
					if [ask "[value $cur_node.name]:\nNo frames found for file input.\nContinue anyway?"] {
						set filename $fileKnob
						set startframe [value root.first_frame]
						set endframe [value root.last_frame]
						} else {return}
					} else {
						set filename [lindex [join $filelist] 0]
						set startframe [lindex [split [lindex [join $filelist] 1] "-"] 0]
						set endframe [lindex [split [lindex [join $filelist] 1] "-"] 1]
						if {$startframe == ""} {set startframe 1}
						if {$endframe == ""} {set endframe 1}
						set foundBase 1
						}
				}
			# PROXY FILE
			if {$proxyKnob != ""} {
				puts "checking proxy file..."
				if {[llength $proxylist] == 0} {
					if [ask "[value $cur_node.name]:\nNo frames found for proxy input.\nContinue anyway?"] {
						set proxyname $proxyKnob
						if ![info exists foundBase] {
							set startframe [value root.first_frame]
							set endframe [value root.last_frame]
							}
						} else {return}
					} else {
						set proxyname [lindex [join $proxylist] 0]
						if ![info exists foundBase] {
							puts "no base file found. setting range based on proxy..."
							set startframe [lindex [split [lindex [join $proxylist] 1] "-"] 0]
							set endframe [lindex [split [lindex [join $proxylist] 1] "-"] 1]
							if {$startframe == ""} {set startframe 1}
							if {$endframe == ""} {set endframe 1}
							}
						}
				}
			} else {
			#SINGLE FRAME
			puts "single rame"
				if {![file exists $fileKnob] && $fileKnob != ""} {
					if ![ask "[value $cur_node.name]:\nNo frame found for file input.\nContinue anyway?"] {
						return
						}
					}
				if {![file exists $proxyKnob] && $proxyKnob != ""} {
					if ![ask "[value $cur_node.name]:\nNo frame found for proxy input.\nContinue anyway?"] {
						return
						}
					}
				set filename $fileKnob
				set proxyname $proxyKnob
				set startframe 1
				set endframe 1
				}
		
		puts "start: $startframe\nend $endframe"
		catch {
			puts "base: $filename"
			set file [list $filename $startframe-$endframe]
			}
		catch {
			puts "proxy: $proxyname"
			set proxy [list $proxyname $startframe-$endframe]	
			}


		if {[info exists file] && [llength $file]} {
			set file [list $filename $startframe-$endframe]
			}
		if {[info exists proxyname] && [llength $proxyname]} {
			set proxyfile [list $proxyname $startframe-$endframe]
			}
		
		if {[info exists proxyfile] && [info exists file]} {
			puts "found base&proxy"
			Read -New file $file proxy $proxyfile
			} elseif [info exists file] {
			puts "found base only"
			Read -New file $file
			} elseif [info exists proxyfile] {
			puts "found proxy only"
			Read -New proxy $proxyfile
			knob [stack 0].first $startframe
			knob [stack 0].last $endframe
			}
			
			
		set newRead [stack 0]
		knob $newRead.xpos [knob $cur_node.xpos]
		knob $newRead.ypos [expr [knob $cur_node.ypos] + 20]
		}
	if ![info exists newRead] {defRead}
	}
