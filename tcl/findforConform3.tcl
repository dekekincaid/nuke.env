# findforConform (plus some other stuff)
# 
#        ...lovingly (RE)writen by Chris Noellert
#
# # Command line Usage:
# # findforConform <edl> <frame rate> <search path> <source mode> <recursion> <edit mode> <accuracy>
#
# # Nuke Gui Usuage:
# # /File/TCL_File... and select this file to parse it.  
# # Menus will automatically be appended to the workspace for the front end tools.
#
# Ok, my scatterbrained documentation....
#
# These are some utils writen originally for other purpose but that I've 
# broken out for playing around with in Nuke.  Everything is work in progress
# but the main guts are starting to shape up. Still very raw.
#
# First of all... the edls have to be CMX3600 A mode and V1 only and I've
# only ever tested it with 24 and 25fps edls...
# I know that blows but hey, we've all got edl manager somewhere right? 
#
# findforConform parses one or more edls into an array called "event"
# Then it systematically... by way of simple brute force and very little
# intelligence finds sourcedirectories for tape sources based on either:
#
# 1. dir (the dir has the name of the tape)
# 2. dir+header (the dir and one of the files inside have the tape name)
# 3. header (a file found contains the correct tape name in the header)
#
# The last argument in the findSource proc is a level of recursion.  This
# is the number of times the proc is allowed to recurse before it gives up.  
#
# Internally, our scan structure looks like:
#
# /path/to/scans/$project/$resolution/$vtape/$vtape_$event.%06d.dpx
#
# So setting the searchpath to say: /path/to/scans/$project/$resolution
# and a recursion of 1 works quite well for me.
#
# Next, it takes the source in timecode and source out timecode and tries
# to locate the event in the directory it's located.
#
# The argument there is whether or not it should check for just the source in tc
# and the source out tc or for every frame in the sequence.
#
# So the choices are:
#
# 1. all (checks every frame between the ins and outs)
# 2. edit (just checks the ins and outs)
#
# To make matters worse or better depending on how you look at it,
# there's also a granularity mode which controls how intensely the code 
# will look for the sequence in question.
#
# So the choices are:
#
# 1. rough (will just look for a tc represented by a frame number in the 
# 	  given frame base for it's match)
# 2. normal (works like rough but also checks the header in the file it finds)
# 3. fine (checks all files in the given directory and checks each of the headers)
#
#
# Whew.
#
# When it's finnished looking, findforConform will throw back the event array
# in the form of an array get command. But not before bombarding the shell with a 
# ton of output... just to let you know it's kicking.
#
# Here's a few examples...
#
# # Dir source, recurses 1 time, event set to "edit ins and outs" and no sourevalidation
# findforConform ./OFFSIDE_AKT1.edl  25 /nfs/smbsrv/scans/OFFSIDE/FULL dir 1 edit rough
#
#
# # Header source, recurses twice, event set to check every frame and sourcevalidation on
# findforConform ./OFFSIDE_AKT1.edl  25 /nfs/smbsrv/scans/OFFSIDE/ header 2 all fine
#
#
# # set an array called event to the output of a findforConform
# # dir+header source, recurses once, checks all frames and no sourcevalidation 
# array set event [findforConform ./OFFSIDE_AKT1.edl  25 /nfs/smbsrv/scans/OFFSIDE/FULL dir+header 1 all normal]
#
# The output for a single event looks like this from a parray:
#
# event(97,comment)                    = NO COMMENT (comment if there was one)
# event(97,filename)                   = V74843_097.%06d.dpx (file sequence name)
# event(97,filenumbering)              = 389991-390022 (frame number in - frame number out)
# event(97,filepath)                   = /nfs/smbsrv/scans/OFFSIDE/FULL/V74843 (abs path to files)
# event(97,id)                         = 97 (array id)
# event(97,keycodein)                  = unmatched (keycode in)
# event(97,keycodeout)                 = unmatched (keycode out)
# event(97,number)                     = 097 (event number from edl)
# event(97,recdur)                     = 31 (record duration)
# event(97,recinframes)                = 97653 (rec in tc converted to frames)
# event(97,recoutframes)               = 97684 (rec out tc converted to frames)
# event(97,rectcin)                    = 01:05:06:03 (rec in tc)
# event(97,rectcout)                   = 01:05:07:09 (rec out tc)
# event(97,sourcedur)                  = 31 (source duration)
# event(97,sourceinframes)             = 389991 (source tcin converted to frames)
# event(97,sourceoutframes)            = 390022 (source tcout converted to frames)
# event(97,sourcetcin)                 = 04:19:59:16 (source tc in)
# event(97,sourcetcout)                = 04:20:00:22 (source tc out)
# event(97,speed)                      = 25 (frame rate) 
# event(97,tape)                       = V74843 (vtape source)
# event(97,title)                      = OFFSIDE_AKT1.edl (edl)
# event(97,track)                      = V (which track)
# event(97,trans)                      = C (event type)
# event(97,transdelta)                 = 0 (transition duration)
#
# The array also contains an entry called (J) which contains how many 
# entries are contained
#
# event(J)                             = 356
#
# To unwind it you can use a little creativity or something like:
#
# foreach n [array names event "*,tape"] { 
#     regexp {^[^,]+} $n j
#     set tape $event($n)
#     set tapes($tape) $j
# }
#
# to pull the tape names...followed by a... 
#
#
# lsort [array names tapes]
#
# ...in a foreach if you we're to need to roll through them. This would be
# useful for something like tails:
#
#
# set frate 25
# array set event [findforConform ./OFFSIDE_AKT1.edl  $frate /nfs/smbsrv/scans/OFFSIDE/FULL dir+header 1 all normal]
#
# foreach n [array names event "*,sourceinframes"] { 
#     regexp {^[^,]+} $n j
#      set sourceinframes $event($n)
#     set sources($sourceinframes) $j
# }
# 
# set tails 10
#
# foreach source [lsort [array names sources]] {
#     set j $sources($source) 
#     set event($j,sourceinframes) [expr $event($j,sourceinframes) - $tails] 
#     set event($j,sourceoutframes) [expr $event($j,sourceoutframes) + $tails]  
#     set event($j,sourcedur) [expr $event($j,sourceoutframes) -  $event($j,sourceinframes) ] 
#     set event($j,sourcetcin) [f2tc $event($j,sourceinframes) $frate ]
#     set event($j,sourcetcout) [f2tc $event($j,sourceoutframes) $frate ]
# }
#
# ...will give you then an entry that's like:
#
# event(97,sourceinframes)             = 389981
#
# ...when it used to be:
#
# event(97,sourceinframes)             = 389991
#
# Aint that cool.
#
# Hmmm.  The code is still work in progress and not such amazing work to begin with, 
# but someone might find it usefull.  Let me know if there's something I should change 
# or some major mis I've made - chris.noellert@mac.com
# 
# The timecode procs was the first thing I ever wrote in tcl... before I knew the joy
# of the format and scan commands.
#
# Things to do:
# Include parseatn and parseale for keycode database matching and avid pulllist support
# General cleanup... things are nasty right now.
# Support for stateside formats
# Add some useful Nuke things to do with the array once it's been made
#
#
# Timecode into frames
# Feed it a timecode and a fps get some frames back
proc tc2f { timecode frame_rate } {
    set secs [expr "1 * $frame_rate"]
    set mins [expr "$frame_rate * 60"]
    set hours [expr "$frame_rate * 60 * 60"]
    set tc [split $timecode ":"] 
    set hrs [lindex $tc 0] ; if { [string index $hrs 0] == 0 } {set hrs [string index $hrs 1]} 
    set mns [lindex $tc 1] ; if { [string index $mns 0] == 0 } {set mns [string index $mns 1]}
    set scs [lindex $tc 2] ; if { [string index $scs 0] == 0 } {set scs [string index $scs 1]}
    set frms [lindex $tc 3] ; if { [string index $frms 0] == 0 } {set frms [string index $frms 1]}
    set frames "[expr "( $hours * $hrs ) + ( $mins * $mns ) + ( $secs * $scs ) + ( $frms )" ]" 
}


# Frames into timecode
# Feed it frames and a framebase and get tc back
proc f2tc { frames frame_rate } {
    set hr [expr $frames / (60 * 60 * $frame_rate)]
    set hrrem [expr $frames % (60 * 60 * $frame_rate)]
    set mn [expr $hrrem / (60 * $frame_rate)]
    set mnrem [expr $hrrem % (60 * $frame_rate)]
    set sc [expr $mnrem / $frame_rate]
    set frm [expr $mnrem % $frame_rate]
    if { [string length "$hr"]==1 } { set hr "0$hr" }
    if { [string length "$mn"]==1 } { set mn "0$mn" }
    if { [string length "$sc"]==1 } { set sc "0$sc" }
    if { [string length "$frm"]==1 } { set frm "0$frm" }
    set tc "$hr:$mn:$sc:$frm"
}

# Timecode math
# Adding or subtracting timecodes at a given fps
# Operations are "+" or "-"
proc tcmath {intc operation outtc frame_rate} {
    set inframes [tc2f $intc $frame_rate]
    set outframes [tc2f $outtc $frame_rate]
    set result [expr $inframes $operation $outframes]
    set resulttc [f2tc $result $frame_rate]
    return $resulttc
}


# Parser for CMX3600 Amode edls
# Returns and array set friendly output
# Only V1 should be on the edl... not audio or all bets are off.
#
# example:
# array set event [parseedl ./test.edl 25]
#
# If there are comments in the form of *2k
# the parser will set the res field to 2k or
# 4k or 1k.
#
proc parseedl { edls frame_rate } {

    set frate $frame_rate

    if { [uplevel #0 array exists event] } {
	  puts "it there"
	  set event(J) [uplevel #0 {subst $event(J)}]
		 set j $event(J)
		 set id $j
	       
	     } {
		 set id 0
		 set event(J) 0
		 set j $event(J)
	     }
  
    foreach fname $edls {
        set title $fname

	if { [catch { open ${fname} r } result] } {
	    set errorMsg $result
	    error "Error opening File: ${errorMsg}"
	}
	
	set fname $result
 
        while { [gets $fname line] >= 0} {
	    incr event(J)
	    set j $event(J) 
	    set event($j,title) [file tail $title]
	    set event($j,number) [lindex $line 0]
	    set event($j,trans) [lindex $line 3]
	    
	    switch $event($j,number) {
		TITLE:   {
		    incr event(J) -1
		}
		
		\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a\u001a {
		    puts "End of EDL encountered"
		    incr event(J) -1 
		}
		
		\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 {
		    puts "End of EDL encountered"
		    incr event(J) -1 
		}
		
		* {
		    incr event(J) -1
		    set j $event(J)
		    set event($j,comment) "$line"
		    set restest [string range $event($j,comment) 2 3]
		    switch $restest { 
			
			2k {
			    set event($j,res) $restest
			}
			2K {
			    set event($j,res) 2k
			}
			4k {
			    set event($j,res) $restest
			}
			4K {
			    set event($j,res) 4k
			}
			1k {
			    set event($j,res) $restest
			}
			1K {
			    set event($j,res) 1k
			}
			
			
			default {
			    set event($j,res) ""
			}
		    }
		}
		
		
		"" {
		    puts "Blank line encountered"
		    incr event(J) -1 
		    }
		    
		"FCM:" {
		    puts "FCM line encountered"
		    incr event(J) -1 
		    }
		
		M2 {
		    puts "Motion effect"
		    incr event(J) -1
		    set j $event(J)
		    
		    set ofr $frame_rate 
		    set m2tape [lindex $line 1]
		    set m2sourcetcin [lindex $line 3]
		    set m2sourceinframes [ tc2f $m2sourcetcin $ofr]
		    set frame_rate [lindex $line 2 ]
		    
		    set frlength [string length $frame_rate]
		    set counter 0
		    if { [string index $frame_rate 0] == "-" } {
			    set gender -
			} {
			    set gender ""
            }
			
#			set absframe_rate format [expr abs($frame_rate)] %d
			set frame_rate ${gender}[format [expr abs($frame_rate)] %d]
		    
		    if { $event($j,sourceinframes_unadjusted) == $m2sourceinframes } {
			puts "Found it.  Source is $event($j,sourceinframes_unadjusted) and m2 source is $m2sourceinframes  "
			if { $frame_rate < 0 } {   
			    #puts "negative"
			    set event($j,sourceoutframes) $event($j,sourceinframes) 
			    set event($j,sourcetcout) $event($j,sourcetcin)
			    set event($j,sourceinframes) [expr [tc2f $event($j,sourcetcout) $ofr] - [expr abs([expr round((([tc2f $event($j,rectcout) $ofr] - [tc2f $event($j,rectcin) $ofr]) * $frame_rate) / $ofr)])]]
			    set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
			    set event($j,sourcetcin) [f2tc $event($j,sourceinframes) $ofr]
			    set event($j,speed) $frame_rate
			} {
			    #puts "positive"
			    set event($j,sourceoutframes) [expr [tc2f $event($j,sourcetcin) $ofr] + [expr round((([tc2f $event($j,rectcout) $ofr] - [tc2f $event($j,rectcin) $ofr]) * $frame_rate) / $ofr)]]
			    set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
			    set event($j,sourcetcout) [f2tc $event($j,sourceoutframes) $ofr]
			    set event($j,speed) $frame_rate
			}
		    } {
			
			
			
			incr event(J) -1
			set j $event(J)
			
			puts "Didn't find it on the first loop - recursing -  Source is $event($j,sourceinframes_unadjusted) and m2 source is $m2sourceinframes  "
			if { $event($j,sourceinframes_unadjusted) == $m2sourceinframes } {
			    puts "Found it.  Source is $event($j,sourceinframes_unadjusted) and m2 source is $m2sourceinframes  "
			    if { $frame_rate < 0 } {   
				#puts "negative"
				set event($j,sourceoutframes) $event($j,sourceinframes) 
				set event($j,sourcetcout) $event($j,sourcetcin)
				set event($j,sourceinframes) [expr [tc2f $event($j,sourcetcout) $ofr] - [expr abs([expr round((([tc2f $event($j,rectcout) $ofr] - [tc2f $event($j,rectcin) $ofr]) * $frame_rate) / $ofr)])]]
				set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
				set event($j,sourcetcin) [f2tc $event($j,sourceinframes) $ofr]
				set event($j,speed) $frame_rate
			    } {
				#puts "positive"
				set event($j,sourceoutframes) [expr [tc2f $event($j,sourcetcin) $ofr] + [expr round((([tc2f $event($j,rectcout) $ofr] - [tc2f $event($j,rectcin) $ofr]) * $frame_rate) / $ofr)]]
				set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
				set event($j,sourcetcout) [f2tc $event($j,sourceoutframes) $ofr]
				set event($j,speed) $frame_rate
			    }
			    incr event(J)
			    set j $event(J)
			    #set transdelta $event($j,transdeltain)
			    #puts $event($j,transdeltain)
			} {
			    if { $event($j,sourceinframes_unadjusted) > $m2sourceinframes } {   
			    puts "Found it.  Source is $event($j,sourceinframes_unadjusted) which is greater than m2 source is $m2sourceinframes  "
				puts $event($j,sourceinframes)
				set event($j,sourceinframes) [expr $event($j,sourceinframes) - [expr abs([expr round([expr ($frame_rate * $transdelta ) / $ofr ])])]]
				set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
				set event($j,sourcetcin) [f2tc $event($j,sourceinframes) $ofr]
				set event($j,speed) $frame_rate
				#puts "$event($j,sourcedur), $event($j,sourcetcin), $event($j,sourcetcout)" 
				
			    } elseif { $event($j,sourceinframes_unadjusted) < $m2sourceinframes } {
				
				puts "Found it.  Source is $event($j,sourceinframes_unadjusted) which is less than m2 source is $m2sourceinframes  "
				set event($j,sourceoutframes) [expr $event($j,sourceinframes) + [expr round([expr ($frame_rate * $transdelta ) / $ofr ])]]
				set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
				set event($j,sourcetcout) [f2tc $event($j,sourceoutframes) $ofr]
				set event($j,speed) $frame_rate
				puts $event($j,sourcedur)
			    }
			}
			
			
		    }
		    set frame_rate $ofr
		}
		
		
		
		
		default {  
		
		    if [string is integer [scan [lindex $line 0] %d]] {
		    
                switch $event($j,trans) {
                
                C {
                    set j $event(J)
                    incr id
                    set event($j,id) $id
                    set event($j,framerate) $frame_rate
                    set event($j,tape) [lindex $line 1]
                    set event($j,track) [lindex $line 2]
                    set event($j,comment) "NO COMMENT"
                    set event($j,transdelta) 0
        
                    set event($j,sourcetcin) [lindex $line 4]
                    set event($j,sourceinframes) [ tc2f $event($j,sourcetcin) $frame_rate]
                    set event($j,sourceinframes_unadjusted) $event($j,sourceinframes)
                
                    set event($j,sourcetcout) [lindex $line 5]
                    set event($j,sourceoutframes) [ tc2f $event($j,sourcetcout) $frame_rate]
                    set lastsourceframesout $event($j,sourceoutframes)
                    
                    set event($j,rectcin) [lindex $line 6]
                    set event($j,recinframes) [ tc2f $event($j,rectcin) $frame_rate]
                    
                    set event($j,rectcout) [lindex $line 7]   
                    set event($j,recoutframes) [ tc2f $event($j,rectcout) $frame_rate]
                    
                    
                    set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
                    set event($j,recdur) [expr $event($j,recoutframes) - $event($j,recinframes)]
                    
                    set event($j,transdelta) 0
                    
                    set event($j,keycodein) unmatched
                    set event($j,keycodeout) unmatched
                    set event($j,filepath)  unknown
                    set event($j,filename) unknown
                    set event($j,filenumbering) unknown
                    
                    
                    set event($j,speed) $frame_rate
                    
                    
                }
                default {
                    
                    incr event(J) -1
                    set j $event(J)
                    
                    set event($j,tape) [lindex $line 1]
                    set event($j,track) [lindex $line 2]
                    set event($j,trans) D
                    set event($j,comment) "NO COMMENT"
                    set event($j,transdelta) [lindex $line 4]
                    set event($j,framerate) $frame_rate
                    
                    set result [regexp {(^|0+)([1-9]+$|[0-9]+)} $event($j,transdelta) 1 2 transdelta ]
                    
                    set event($j,transdelta) $transdelta 
                    
                    set event($j,sourcetcin) [lindex $line 5] 
                    set event($j,sourceinframes) [ tc2f $event($j,sourcetcin) $frame_rate]
                    set event($j,sourceinframes_unadjusted) [ tc2f $event($j,sourcetcin) $frame_rate]
                    
                    set event($j,sourcetcout) [lindex $line 6]
                    set event($j,sourceoutframes) [ tc2f $event($j,sourcetcout) $frame_rate]
                    
                    set event($j,rectcin) [lindex $line 7]
                    set event($j,recinframes) [ tc2f $event($j,rectcin) $frame_rate]
                    
                    set event($j,rectcout) [lindex $line 8]
                    set event($j,recoutframes) [ tc2f $event($j,rectcout) $frame_rate]
                    
                    set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
                    set event($j,recdur) [expr $event($j,recoutframes) - $event($j,recinframes)]
                    
                    set event($j,transintcin) $event($j,rectcin)
                    set event($j,transintcout) [ f2tc [ expr $event($j,recinframes) + $transdelta ] $frame_rate ]
                    
                    set event($j,keycodein) unmatched
                    set event($j,keycodeout) unmatched
                    set event($j,filepath)  unknown
                    set event($j,filename) unknown
                    set event($j,filenumbering) unknown
                    
                    
                    set event($j,speed) $frame_rate
                    
                    incr event(J) -1
                    set j $event(J)
                    
                    if { $j != 0 } {
                    if { "$lastsourceframesout" == "$event($j,sourceoutframes)" } {
                        
                        set event($j,sourceoutframes) [expr $event($j,sourceoutframes) + $transdelta]
                        set event($j,sourcetcout) [ f2tc $event($j,sourceoutframes)  $frame_rate]
                        set event($j,recoutframes) [expr $event($j,recoutframes) + $transdelta]
                        set event($j,rectcout) [ f2tc $event($j,recoutframes)  $frame_rate]
                        set event($j,sourcedur) [expr $event($j,sourceoutframes) - $event($j,sourceinframes)]
                        
                        
                    }
                    }	
                    
                    incr event(J)
                    set j $event(J)
                    set lastsourceframesout $event($j,sourceoutframes)
    
                }
                }
            } {
                puts "End of EDL encountered"
                incr event(J) -1 
            }
		    
		}
	    }
        }
        close $fname
    }
    return [array get event]
}

# Return the sourcefield from a Correct dpx header.. 
proc dpxSource { fileName } {
   
    if { [catch { open ${fileName} r } result] } {
	set errorMsg $result
	error "Error opening File: ${errorMsg}"
    }
     
    set fileHandle $result
    fconfigure ${fileHandle} -encoding binary
    
    set header [read ${fileHandle} 16384]
    catch { close $fileHandle }
    binary scan ${header} @1556A32 source
    
    if {![info exists source]} {
	set source unknown
    } {
	regexp {\w+} $source newsource
	set source $newsource
    }
    return $source
}

# Returns the timecode from a dpx header...
proc dpxTc { fileName } {

    if { [catch { open ${fileName} r } result] } {
	set errorMsg $result
	error "Error opening File: ${errorMsg}"
    }
     
    set fileHandle $result
    fconfigure ${fileHandle} -encoding binary
    
    set header [read ${fileHandle} 16384]
    catch { close $fileHandle }
    binary scan ${header} @1920i1 inttc
    
    if {[info exists inttc]} {
    
	set val $inttc 
	
	set ff	[format "%0x" [expr { ( $val >> 24 ) & 0xFF }]]
	set ss	[format "%0x" [expr { ( $val >> 16 ) & 0xFF }]]
	set mm	[format "%0x" [expr { ( $val >>  8 ) & 0xFF }]]
	set hh	[format "%0x" [expr { $val & 0xFF }]]
	
	set tc [format "%02d:%02d:%02d:%02d" ${hh} ${mm} ${ss} ${ff}]
    } {
	set tc "00:00:00:00"
    }
    return $tc
}
# Finds an event 
#
# Mode is either:
# edit (for checking just the in and the out) or
# all (for checking every frame between the in and out)
# Then feed it ins, outs, fps and a path to look.
#
# Accuracy is either fine(slow), normal(faster) or rought(fast) ;)
# Fine and normal accuracy require an additional argument which 
# is the source to validate against in the header of the proposed
# dpx match.  Fine will in addition to header matching also check
# through every file in the directory whereas normal will look for 
# a framenumber which is the tc converted in the indicated frame rate.
#
# Rough is the nicest one if the scans are done right because it just
# pings for the tc converted to framenumber and doesn't check against
# the header.  So it goes fast... 
#
# example in rough mode:
# findEvent all 01:02:03:04 01:02:04:05 25 /where/it/should/be rough
#
# example with normal:
# findEvent all 01:02:03:04 01:02:04:05 25 /where/it/should/be normal VT18041
# 
# On sucess it returns a list in the form of:
# matched {/where/it/should/be/prefix.padding.dpx framein-frameout}
#
# And on failure it looks like this:
# unmatched {Edit not fount: Failed to locate source in-point $sourcetcin}
#
proc findEvent {mode_ sourcetcin sourcetcout framerate searchpath accuracy {args}} {

    if { [llength $args] > 0 } {
	set source [concat [lindex $args end]]
    }

    switch -exact $accuracy {
	
	rough {
	    set accuracy 0
	    set sourcevalidation 0
	}
	
	normal {
	    set accuracy 0
	    set sourcevalidation 1
	}
	
	fine {
	    set accuracy 1
	    set sourcevalidation 1
	}
    }
	
    set status unmatched
    
    if {$sourcevalidation} {
	set returninfo "Edit not fount: Failed to locate source in-point $sourcetcin \nwith originator $source"
    } {
	set returninfo "Edit not fount: Failed to locate source in-point $sourcetcin"
    }

    if { ![file isdirectory $searchpath] } {
		set errorMsg "Search directory does not exist"
		error "Error opening Directory: ${errorMsg}"
	}


    switch -exact $sourcevalidation {

	
	1 {
	    #Validate the header source
	    
	    
	    if { $accuracy } {

		set flist [concat [lsort  [glob -nocomplain -dir $searchpath -tails *.dpx]]]
	    } {

		set ftestfnumber [tc2f $sourcetcin $framerate]
		set flist [concat [lsort  [glob -nocomplain -dir $searchpath -tails *${ftestfnumber}.dpx]]]
	    }
	    
	    if {$flist > 0} {
		puts "File list for dirictory [lindex [split  $searchpath /] end] aquired.  \nSearching for timecodes $sourcetcin - $sourcetcout ..." 
		for {set pos 0} {$status != "matched" && $pos < [llength $flist] } {incr pos} {
		    
		    set f  [lindex $flist $pos]
		    
		    set tc [dpxTc [file join $searchpath $f]]
		    
		    
		    set framesin [tc2f $sourcetcin $framerate]
		    set framesout [tc2f $sourcetcout $framerate]
		    
		    set filesource [dpxSource [file join $searchpath $f]] 
		    
		    
		    set fsplit [split $f "."]
		    
		    set sourceframein [scan [lindex $fsplit end-1] %d]
		    
		    set padding [string length [lindex $fsplit end-1]] 
		    
		    
		    set prefix [lindex $fsplit end-2]
		    
		    
		    set sourceframeout [expr ([tc2f $sourcetcout $framerate] - [tc2f $sourcetcin $framerate]) + $sourceframein ]
		    
		    if {[string length $prefix] > 0} {
			
			set fin "$prefix.[format "%0${padding}d" $framesin].dpx"
			set fout "$prefix.[format "%0${padding}d" $sourceframeout].dpx"
			
		    } {
			set fin "[format "%0${padding}d" $framesin].dpx"
			set fout "[format "%0${padding}d" $sourceframeout].dpx"
			
		    }
		    
		    
		    
		    if {$tc == $sourcetcin && $filesource == $source} {
			
			
			
			if {
			    [file exists [file join $searchpath $fout]] == 1 && 
			    [dpxTc [file join $searchpath $fout]] == $sourcetcout &&
			    [dpxSource [file join $searchpath $fout]] == $source
			} {
			    puts "Source header in out file validated... proceeding"
			    switch -exact -- ${mode_} {
				
				edit {			
				    
				    if {[string length $prefix] > 0} {
					set returninfo [list [file join $searchpath $prefix.%0${padding}d.dpx] $sourceframein-$sourceframeout]
					set status matched
				    } { 
					set returninfo [list [file join $searchpath %0${padding}d.dpx] $sourceframein-$sourceframeout]
					set status matched
				    }
				}
				
				all {
				    
				    set substatus 1
				    for {set fnumber $sourceframein} { $fnumber <= $sourceframeout } { incr fnumber } {
					
					if {[string length $prefix] > 0} {
					    set ftest "$prefix.[format "%0${padding}d" $fnumber].dpx"
					} { 
					    set ftest "[format "%0${padding}d" $fnumber].dpx"
					}
					
					set ftesttc [f2tc [expr [tc2f $tc $framerate] + ($fnumber - $sourceframein)] $framerate]
					
					if {
					    ![file exists [file join $searchpath $ftest]] || 
					    [dpxTc [file join $searchpath $ftest]] != $ftesttc ||
					    [dpxSource [file join $searchpath $ftest]] != $source 
					} then {
					    set substatus 0
					    set returninfo "Edit Not Found: Failed to locate sequential timecode $ftesttc with source $source"
					    break
					}
				    }
				    
				    
				    if { $substatus == 1 } {
					if {[string length $prefix] > 0} {
					    set returninfo [list [file join $searchpath $prefix.%0${padding}d.dpx] $sourceframein-$sourceframeout]
					    set status matched
					} { 
					    set returninfo [list [file join $searchpath %0${padding}d.dpx] $sourceframein-$sourceframeout]
					    set status matched
					}
					
				    } 
				}
			    }
			}		  
		    }
		    if {$status == "matched" } {
			puts "Timecodes $sourcetcin - $sourcetcout located... breaking"
			break
		    }	
		}

	    }
	    
	    
	}  
	
	
	0 {
	    #Don't bother to validate the header source
 
	    set ftestfnumber [tc2f $sourcetcin $framerate]
	    set flist [concat [lsort  [glob -nocomplain -dir $searchpath -tails *${ftestfnumber}.dpx]]]
	    
	    if {$flist > 0} {
		
		puts "File list for dirictory [lindex [split  $searchpath /] end] aquired.  \nSearching for timecodes $sourcetcin - $sourcetcout ..." 
		for {set pos 0} {$status != "matched" && $pos < [llength $flist] } {incr pos} {
		    
		    set f  [lindex $flist $pos]
		    
		    set framesin [tc2f $sourcetcin $framerate]
		    set framesout [tc2f $sourcetcout $framerate]
		    set fsplit [split $f "."]
		    set sourceframein [scan [lindex $fsplit end-1] %d]
		    set padding [string length [lindex $fsplit end-1]] 
		    set prefix [lindex $fsplit end-2]
		    set sourceframeout [expr ([tc2f $sourcetcout $framerate] - [tc2f $sourcetcin $framerate]) + $sourceframein ]
		    
		    if {[string length $prefix] > 0} {
			
			set fin "$prefix.[format "%0${padding}d" $framesin].dpx"
			set fout "$prefix.[format "%0${padding}d" $sourceframeout].dpx"
			
		    } {
			set fin "[format "%0${padding}d" $framesin].dpx"
			set fout "[format "%0${padding}d" $sourceframeout].dpx"
			
		    }
		    
		    
		    if {
			[file exists [file join $searchpath $fout]] == 1
		    } {
			switch -exact -- ${mode_} {
			    
			    edit {			
				if {[string length $prefix] > 0} {
				    set returninfo [list [file join $searchpath $prefix.%0${padding}d.dpx] $sourceframein-$sourceframeout]
				    set status matched
				} { 
				    set returninfo [list [file join $searchpath %0${padding}d.dpx] $sourceframein-$sourceframeout]
				    set status matched
				}
			    }
			    
			    all {
				#check all frames between startframe and endframe
				
				set substatus 1
				
				for {set fnumber $sourceframein} { $fnumber <= $sourceframeout } { incr fnumber } {
				    if {[string length $prefix] > 0} {   
					
					set ftest "$prefix.[format "%0${padding}d" $fnumber].dpx"
				    } { 
					set ftest "[format "%0${padding}d" $fnumber].dpx"
				    }
				    
				    if {
					![file exists [file join $searchpath $ftest]]
				    } then {
					set substatus 0
					set returninfo "Edit Not Found: Failed to locate sequential timecode $ftesttc"
					break
				    }
				}
				
				
				if { $substatus == 1 } {
				    if {[string length $prefix] > 0} {
					set returninfo [list [file join $searchpath $prefix.%0${padding}d.dpx] $sourceframein-$sourceframeout]
					set status matched
				    } { 
					set returninfo [list [file join $searchpath %0${padding}d.dpx] $sourceframein-$sourceframeout]
					set status matched
				    }
				    
				} 
			    }
			}
		    }		  
		    if {$status == "matched" } {
			puts "Timecodes $sourcetcin - $sourcetcout located... breaking"
			break
		    }	
		}
	    } 
	}
    }
    
    return [list $status $returninfo]
}
# finds a source direcotry relating to a vtapesource in an edl...
#
# Mode is either:
# 1. dir (for just matching a dir name... and the name has to be exact)
#
# 2. dir+header (which will match a dir name and then try to locate a 
#    dpx file that has the same sourcename in the header to verify)
# 
# 3. header {which only looks for a dpxfile with the correct header source)
#
# Source is the source needed to match, searchpath is where to look.
# The args at this point are just recurion but will later be sub recursion
# as well.  But that's text for another comment region another day.
# The recursion is how many levels the proc is allowed to decend from 
# the original search path to find the source.  Which can be handy. 
#
# examples:
#
# find a header source for VT18401 where I am now recursing 2 levels
# findSource header VT18401 [pwd] 2
# 
# find a dir source verified by a contained dpx file with source bajs from 
# where I am now and recursing 1 directory:
# findSource dir+header bajs [pwd] 1
#
# findSource returns a list regardless in the form of:
# matched /path/to/dir/bajs
#
# for a match and...
# unmatched {Source not fount: Failed to locate source bajs}
#
#
# if it fails.  Regardless it's quite verbose about what's going on...
#
proc findSource { mode_ source searchpath {args} } {
    
    set status unmatched
    set returninfo "Source not fount: Failed to locate source $source"
    
    if { ![file isdirectory $searchpath] } {
       	set errorMsg "Search directory does not exist"
	error "Error opening Directory: ${errorMsg}"
    }
    
   
    set recursion [lindex ${args} 0]

    if {[llength ${args}] > 1} {
	set srecursion [lindex ${args} 1]
    }
    
    switch -exact ${mode_} {
	    
	dir {
	    
	    if { $status != "matched" } {
		if {
		    [llength  [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d ${source}]]]] > 0
		} then {
		    set destpath "[file join $searchpath [lindex [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d ${source}]]] 0]]"
		    set status matched 
		    set returninfo "$destpath" 
		    puts "Located directory source $source in $destpath.  Exiting..."
		} {
		    set dirlist [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d *]]]
		    
		    foreach dir $dirlist {
			
			if { [expr $recursion -1] >= 0 } {
			    puts "Searching in [file join $searchpath $dir] for source $source"
			    set looprecursion [expr $recursion - 1]
			    set result [findSource ${mode_} $source [file join $searchpath $dir] $looprecursion]
			    
			    if {[lindex $result 0] == "matched" } {
				set status matched
				set returninfo "[lindex $result 1]"
				break
			    }
			}
		    }
		}
	    }
	}
	    
	dir+header {
		
	    if { $status != "matched" } {
		if {
		    [llength  [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d ${source}]]]] > 0
			
		} then {


		    
		    set destpath "[file join $searchpath [lindex [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d ${source}]]] 0]]"
		    
		    set flist [concat [lsort  [glob -nocomplain -dir $destpath -tails *.dpx]]]
			
		    foreach f $flist {
			    
			set fsource [dpxSource [file join $destpath $f]]
			
			if { $fsource == $source } {
				
			    set status matched 
			    set returninfo "$destpath" 
			    puts "Located directory source $source in $destpath. \nMatch has been verified agaist the dpx header of file $f.  Exiting..."
			    break
			}
		    }
		    
		} {
		    set dirlist [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d *]]]
		    
		    foreach dir $dirlist {
			
			if { [expr $recursion -1] >= 0 } {
			    puts "Searching in [file join $searchpath $dir] for source $source"
			    set looprecursion [expr $recursion - 1]
			    set result [findSource ${mode_} $source [file join $searchpath $dir] $looprecursion]
			    
			    if {[lindex $result 0] == "matched" } {
				set status matched
				set returninfo "[lindex $result 1]"
				break
			    }


			}
		    }
		}
	    }
	}
	
	header {
	    
	    if { $status != "matched" } {
		
		set flist [concat [lsort  [glob -nocomplain -dir $searchpath -tails *.dpx]]]
		
		foreach f $flist {
		    
		    set fsource [dpxSource [file join $searchpath $f]]
		    
		    if { $fsource == $source } {
			
			set status matched 
			set returninfo "$searchpath" 
			puts "Located directory source $source in $searchpath. \nMatch has been verified agaist the dpx header of file $f.  Exiting..."
			break
		    }
		}
		
		set dirlist [concat [lsort  [glob -nocomplain -dir $searchpath -tails -type d *]]]
		
		
		foreach dir $dirlist {
		    
		    if { [expr $recursion -1] >= 0 } {
			puts "Searching in [file join $searchpath $dir] for source $source"
			set looprecursion [expr $recursion - 1]
			set result [findSource ${mode_} $source [file join $searchpath $dir] $looprecursion]
			
			if {[lindex $result 0] == "matched" } {
			    set status matched
			    set returninfo "[lindex $result 1]"
			    break
			}
		    }
		}
	    }
	}
    }
    return  "[list $status $returninfo]"
}


#Instructions at the top... Bon Chance.
#
proc findforConform { edls framerate searchpath {args}} {
    
    set sourcemode [lindex ${args} 0]
    set recursion [lindex ${args} 1]
    set eventmode [lindex ${args} 2] 
    set accuracy [lindex ${args} 3]

    switch -exact $accuracy {
	
	rough {
	    set sourcevalidation 0
	}
	
	normal {
	    set sourcevalidation 1
	}
	
	fine {
	    set sourcevalidation 1
	}
    }
	

    array set event [parseedl $edls $framerate]
    
    foreach n [array names event "*,sourceinframes"] { 
        regexp {^[^,]+} $n j
        set sourceinframes $event($n)
        set sources($sourceinframes) $j
    }
    
    foreach n [array names event "*,tape"] {
        regexp {^[^,]+} $n j
        set tape $event($n)
        set tapes($tape) $j
    }
    
    foreach tape [lsort [array names tapes]] {

	set sourceresults [findSource $sourcemode $tape $searchpath $recursion]
		
	if {[lindex $sourceresults 0] == "matched"} {

	    set sourcepath [lindex $sourceresults 1]
	    
	    foreach source [lsort -integer [array names sources]] {
		set j $sources($source) 
		
		if { $event($j,tape) == $tape } {
		
		    if { $sourcevalidation } {
		    
			set clipresults [findEvent $eventmode $event($j,sourcetcin) $event($j,sourcetcout) $framerate $sourcepath $accuracy 1 $tape] 
		    } {
			set clipresults [findEvent $eventmode $event($j,sourcetcin) $event($j,sourcetcout) $framerate $sourcepath $accuracy]
		    }
		    
		    if {[lindex $clipresults 0] == "matched" } {
			set path [lindex [lindex $clipresults 1] 0]
			set numbering [lindex [lindex $clipresults 1] 1]
			
			set event($j,filepath) [file dirname $path]
			set event($j,filename) [file tail $path]
			set event($j,filenumbering) $numbering
			set event($j,sourcemode) source
			
		    } {
			set event($j,filepath)  unknown
			set event($j,filename) unknown
			set event($j,filenumbering) unknown
		    set event($j,sourcemode) source
		    }
		    
		}
	    }
	}   
    }
    return [array get event]
} 



proc splitforConform { edls framerate clip} {

    set path [lindex [lindex $clip 0] 0]
	set numbering [lindex [lindex $clip 0] 1]
    
    set in [lindex [split $numbering "-"] 0]
    set out [lindex [split $numbering "-"] 1]
    
    array set event [parseedl $edls $framerate]
    
    foreach n [array names event "*,recinframes"] { 
        regexp {^[^,]+} $n j
        set recinframes $event($n)
        set recs($recinframes) $j
    }
    
    if { $in == "" } {
        set prevout [expr $in - 0]
    } {
        set prevout [expr $in - 1]
    }
    
    foreach rec [lsort -integer [array names recs]] {
        set j $recs($rec) 
            
        set duration [expr $event($j,recoutframes) - $event($j,recinframes) - 1]
        set newIn [expr $prevout +1]
        set newOut [expr $newIn + $duration]
        set prevout $newOut
        
        set numberingNew "${newIn}-${newOut}"
        
        set event($j,filepath) [file dirname $path]
        set event($j,filename) [file tail $path]
        set event($j,filenumbering) $numberingNew
        set event($j,sourcemode) rec
        set event($j,clipinfo) $clip
    }   
    return [array get event]
} 


# Nuke side....
# This proc creates a Nuke panel for interfacing into findforConform as
# as well as parseedl.  Select your edl, fps and other parameters and 
# lock and load.
#
proc edlEntry {} {
    global env
    global event
    global edls
    if [info exists event] {
	if {
	    [ask "Clear Existing edlEvents?"]
	} {
	    unset event
	}
    }
    
    if [info exists env(USERNAME)] {set inputEdl "/job/HOME/$env(USERNAME)/.nuke/"}
    if [info exists env(TEMP)] {set searchDir "$env(TEMP)"}
    
    set sourcemode dir+header
    set editmode all

    set recursion 1
    set frameRate 25


    if [catch {panel -w500 "Parse EDL" {
	{"Input EDL:" inputEdl f}
	{"Frame rate:" frameRate e {24 25 30}}
	{"EDL Type:" listType e {"Source Timecode" "Record Timecode"}}
	{"Search for Events?" search b}
    }}] {
	message {Parse has been cancelled}
    } {
	switch $search {
	    
	    1 {
	    
	        switch $listType {
	        
	           "Source Timecode" { 
	        
                    if [catch {panel -w500 "Source EDL Search Options" {
                    {"Search path: " searchDir f}
                    {"Levels of recursion:" recursion}
                    {"Source mode:" sourceMode e {dir dir+header header}}
                    {"Edit check mode:" editMode e {all edit}}
                    {"Accuracy:" sourceVal e {rough normal fine}}
                    }}] {
                        message {Parse has been cancelled}
                    } {
                    
                    if {
                        [ask "Are you sure you want to parse and loacte events for [file tail $inputEdl]?"] 	
                    } {
                        array set event [findforConform $inputEdl $frameRate $searchDir $sourceMode $recursion $editMode $sourceVal]
                        set statement "menu \"edl->Nuke/Add/Conform/[file tail $inputEdl] - SOURCE mode\" \{ edlConformSource [list $inputEdl $clipSelection]\}"
                        eval $statement
                        message "Parsing and find of events for [file tail $inputEdl] completed..."
                    } {
                        message {Parse and Find has been cancelled}
                    }
	               }
	            }
	            
                "Record Timecode" { 
	        
                    if [catch {get_clipname "Choose Previously Assembled Clip" } clipSelection ] { 
                        message {Parse has been cancelled}
                    } {
                            
                    if {
                        [ask "Are you sure you want to parse and loacte events for [file tail $inputEdl]?"] 	
                    } {
                        array set event [splitforConform $inputEdl $frameRate $clipSelection]                        
                        set statement "menu \"edl->Nuke/Add/Conform/[file tail $inputEdl] - REC mode\" \{ edlConformRec [list $inputEdl $clipSelection]\}"
                        eval $statement

                        set statement "menu \"edl->Nuke/Add/Media/[file tail $inputEdl] - REC mode\" \{ edlEvent [file tail $inputEdl]\}"
                        eval $statement
                        
                        message "Parsing and find of events for [file tail $inputEdl] completed..."
                    } {
                        message {Parse and Find has been cancelled}
                    }
	               }
	            }
            }
            }
	    
	    0 {
		
		if {
		    [ask "Are you sure you want to parse [file tail $inputEdl]?"] 	
		} {
		    array set event [parseedl $inputEdl $frameRate]
		    
		    message "Parsing events for [file tail $inputEdl] completed..."
		} {
		    message {Parse has been cancelled}
		}
	    }
	    
	}
    }
}
# edlEvent creates a series of panels that guide the user
# through selecting a source/event from the parsed edl into
# the nuke workspace.  First the user choose from which edl
# to pulll the cut, how to organize the resulting list of 
# cuts, and what attributes will be visible.  Then the proc
# creates a list of available events to choose from, commented
# by their attributes.  The user picks one cut, hits "ok" and 
# the source for the event (provided it has been located during 
# the search will be added to the Nuke workspace as a read node.
#  
proc edlEvent { edlChoice } {
    global env
    global event
    
    
    if { [info exists event] } {
	
    	set statement "panel \"Add edlEvent for [file tail $edlChoice]\" { { \"Sort list\" sortChoice e {Amode Cmode}} { \"List Vtape\" vtapeChoice b } { \"List SourceTC\" sourceChoice b } { \"List RecTC\" recChoice b }}"
	
        if [catch { eval $statement }] {
            message {edlEvent Addition has been cancelled}
        } {
            switch $sortChoice {
            
            Cmode {
    
                foreach n [array names event "*,tape"] { 
                regexp {^[^,]+} $n j
                  set tape $event($n)
                set tapes($tape) $j
                }
                
                foreach n [array names event "*,sourceinframes"] { 
                regexp {^[^,]+} $n j
                set sourceinframes $event($n)
                set sources($sourceinframes) $j
                }  
                
                foreach tape [lsort [array names tapes]] {
                foreach source [lsort -integer [array names sources]] {
                    set j $sources($source) 
                    if { $event($j,tape) == $tape && $event($j,title) == $edlChoice  } {
                    
                    set cutStatement "Event: $event($j,number)"
                    
                    if {$vtapeChoice} {
                        set cutStatement "$cutStatement Vtape: $event($j,tape)"
                    }
                    
                    if {$sourceChoice} {
                        set cutStatement "$cutStatement SourceTC: $event($j,sourcetcin)-$event($j,sourcetcout)"
                    }
                    
                    if {$recChoice} {
                        set cutStatement "$cutStatement RecordTC: $event($j,rectcin)-$event($j,rectcout)"
                    }
                    
                    lappend cuts $cutStatement
                    lappend cutsIds $event($j,id)
                    }
                }
                }
            }
            
            Amode {
               
                
                foreach n [array names event "*,recinframes"] { 
                regexp {^[^,]+} $n j
                set recinframes $event($n)
                set recs($recinframes) $j
                }
                
                foreach source [lsort -integer [array names recs]] {
                
                set j $recs($source)
                
                if { $event($j,title) == $edlChoice  } {
                    
                    set cutStatement "Event: $event($j,number)"
                    
                    if {$recChoice} {
                    set cutStatement "$cutStatement RecordTC: $event($j,rectcin)-$event($j,rectcout)"
                    }
                    
                    if {$vtapeChoice} {
                    set cutStatement "$cutStatement Vtape: $event($j,tape)"
                    }
                    
                    if {$sourceChoice} {
                    set cutStatement "$cutStatement SourceTC: $event($j,sourcetcin)-$event($j,sourcetcout)"
                    }
                    
                    lappend cuts $cutStatement
                    lappend cutsIds $event($j,id)
                }
                }
            }
            }
            
            set statement2 "panel \"Add selected edlEvent\" {{ \"Select edlEvent\" eventSelection e { $cuts }}}"
    
            if [catch { eval $statement2 }]  {
            message {edlEvent Addition unexpectedly canceled}
            } {
            set match [lsearch $cuts $eventSelection]
            if { $match >= "0" } {
                set idMatch [lindex $cutsIds $match]
                addSource $idMatch
            } {
                message "Failed to add Read node for Source"
            }
            
            }
             
        }
    }
}
#
proc edlConformSource { edlChoice } {
    global env
    global event
    
    
    if { [info exists event] } {

	
        foreach n [array names event "*,recinframes"] { 
            regexp {^[^,]+} $n j
            set recinframes $event($n)
            set recs($recinframes) $j
        }
		
		
		
        foreach source [lsort -integer -decreasing [array names recs]] {
			
			set j $recs($source)
		    set framerate $event($j,framerate)
			set inFrame [lindex [split $event($j,filenumbering) "-"] 0]
			set outFrame [lindex [split $event($j,filenumbering) "-"] 1]
			set fileName [file join $event($j,filepath) $event($j,filename)]
			set sourceMode $event($j,sourcemode)
			
			if { $event($j,title) == $edlChoice && [info exists event($j,transdelta)] } {
                        
                if { $event($j,tape) != "BL" } {
                    
                    
                    set statement "Read \{ inputs 0 file $fileName first $inFrame before black last $outFrame after black first_lock true last_lock true name \"Media $event($j,number) [file tail $event($j,filename)]\" \}"
                    eval $statement
                    lappend conformStatement  "Read \{ inputs 0 file $fileName first $inFrame before black last $outFrame after black name \"Media $event($j,number) [file tail $event($j,filename)]\" \}"
                    
                    if { 0 >= $event($j,speed) && $sourceMode != "rec" && [info exists event($j,transdelta)] } {
                        set inDelta [expr $outFrame - $inFrame]
                        set outDelta [expr $event($j,recoutframes) - $event($j,recinframes)]
                        set speed [expr -1 * (${inDelta}.0 / $outDelta)]
                                                
                        set statement "Retime \{ input.first $inFrame input.last $outFrame reverse true output.first $inFrame output.last [expr $inFrame + $outDelta] speed $speed shutter 0 name \"Retime $event($j,number) [file tail $event($j,filename)]\" \}"
                        eval $statement
                        lappend conformStatement  "Retime \{ input.first $inFrame input.last $outFrame reverse true output.first $inFrame output.last [expr $inFrame + $outDelta] speed $speed shutter 0 name \"Retime $event($j,number) [file tail $event($j,filename)]\" \}"
    
                    } elseif { $event($j,speed) > 0 && $framerate != $event($j,speed) && $sourceMode != "rec" && [info exists event($j,transdelta)] } {

                        set inDelta [expr $outFrame - $inFrame]
                        set outDelta [expr $event($j,recoutframes) - $event($j,recinframes)]
                        set speed [expr ${inDelta}.0 / $outDelta]
                                                
                        set statement "Retime \{ input.first $inFrame input.last $outFrame reverse false output.first $inFrame output.last [expr $inFrame + $outDelta] speed $speed shutter 0 name \"Retime $event($j,number) [file tail $event($j,filename)]\" \}"
                        eval $statement
                        lappend conformStatement  "Retime \{ input.first $inFrame input.last $outFrame reverse false output.first $inFrame output.last [expr $inFrame + $outDelta] speed $speed shutter 0 name \"Retime $event($j,number) [file tail $event($j,filename)]\" \}"
    
                    }
                    
                } elseif { $event($j,name) == "BL" && $sourceMode != "rec" && [info exists event($j,transdelta)] } {
                    
                    set statement "Constant { inputs 0 channels rgb first $event($j,recinframes) last $event($j,recoutframes) name \"Slug\"}" 
                    eval $statement
                    lappend conformStatement "Constant { inputs 0 channels rgb first $event($j,recinframes) last $event($j,recoutframes) name \"Slug\"}"                   
                
                }   
                
            }
        }
        
        foreach source [lsort -increasing -integer [array names recs]] {
                
            set j $recs($source)

            set k [expr $j + 1]
            
            if { [info exists event($k,transdelta)] } {
                if { $event($k,trans) != "C" && $event($k,transdelta) > 0 } {
                    set dissolve [expr $event($j,transdelta) + 1]
                    set statement "AppendClip \{inputs 2 dissolve $dissolve name \"Event [expr $j + 1]\"\}"
                    eval $statement
                    lappend conformStatement "AppendClip \{inputs 2 dissolve $dissolve name \"Event [expr $j + 1]\"\}"
                } {
                    set dissolve 0
                    set statement "AppendClip \{inputs 2 dissolve $dissolve name \"Event [expr $j + 1]\"\}"
                    eval $statement
                    lappend conformStatement "AppendClip \{inputs 2 dissolve $dissolve name \"Event [expr $j + 1]\"\}"
                }
            } 
        } 
    }
}

#
proc edlConformRec { edlChoice clip } {
    global env
    global event
    
    puts $clip  
    
    set clipName [lindex $clip 0]
    set clipNumbering [lindex $clip 1]
    
    set clipIn [lindex [split $clipNumbering "-"] 0]
    set clipOut [lindex [split $clipNumbering "-"] 1]
    
    
    if { [info exists event] } {
    
        foreach n [array names event "*,recinframes"] { 
            regexp {^[^,]+} $n j
            set recinframes $event($n)
            set recs($recinframes) $j
        }
		
		set statement "Read \{ inputs 0 file $clipName first $clipIn last $clipOut name \"Assembly [file tail [lindex $clipName 0]]\" \}"
        eval $statement
        
        set statement "set assembly \[stack 0\]"
        eval $statement
		
        foreach source [lsort -integer -decreasing [array names recs]] {
			
			set j $recs($source)
		    set framerate $event($j,framerate)
			set inFrame [lindex [split $event($j,filenumbering) "-"] 0]
			set outFrame [lindex [split $event($j,filenumbering) "-"] 1]
			set fileName [file join $event($j,filepath) $event($j,filename)]
			set sourceMode $event($j,sourcemode)
			
			
			if { $event($j,title) == [file tail $edlChoice] && [info exists event($j,transdelta)] } {
                        
                set statement "FrameRange \{ first_frame $inFrame last_frame $outFrame name \"Assembly [file tail [lindex $clipName 0]]\" \}"
                eval $statement
                
                set statement "set lastnode \[stack 0\]"
                eval $statement

                if { [scan $event($j,number) %d] != "1" } {
                    set statement "push $assembly"
                    eval $statement

                }
            }
        }
        
        foreach source [lsort -increasing -integer [array names recs]] {
                
            set j $recs($source)

            set k [expr $j + 1]
            
            if { $event($j,title) == [file tail $edlChoice] && [info exists event($k,transdelta)] } {
                if { $event($k,trans) != "C" && $event($k,transdelta) > 0 } {
                    set dissolve [expr $event($j,transdelta) + 1]
                    set statement "AppendClip \{inputs 2 dissolve $dissolve name \"Event [expr $j + 1]\"\}"
                    eval $statement
                } {
                    set dissolve 0
                    set statement "AppendClip \{inputs 2 dissolve $dissolve name \"Event [expr $j + 1]\"\}"
                    eval $statement
                }
            } 
        } 
        set counter 0

    }
    return Complete
}
# Support proc for adding the read node to the workspace based
# on a given id baked into each entry in the event array.
#	
proc addSource { id } {
    global env
    global event

    set inFrame [lindex [split $event($id,filenumbering) "-"] 0]
    set outFrame [lindex [split $event($id,filenumbering) "-"] 1]
    set fileName [file join $event($id,filepath) $event($id,filename)]

    set statement "Read \{ inputs 0 file $fileName first $inFrame before black last $outFrame after black name \"Media $event($id,number) [file tail $event($id,filename)]\" \}"
    eval $statement
}
# Nuke menu entries to keep thing easy
#
set statement "menu \"edl->Nuke/Import/Import edl\" \{ edlEntry\}"
eval $statement

    
    