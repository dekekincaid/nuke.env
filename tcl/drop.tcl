##############################
# bit of Spaghetti code by Frank Rueter
# This function is called when the user drag'n'drops something on the main window.
# Needs "compressList2.tcl" installed in Nuke's plugin path
# Needs "expandList.tcl" installed in Nuke's plugin path
# last changed Sept/12/2006
#    -fixed "*" at end of file name
#
# added functionality:
#    -obj support
#    -chan support (camera or axis depending on file content)
#    -dialog to chose between multiple Read nodes and sequence compression (when multiple frames are dropped)
#    -optional preference file to control the following behaviour:
#        silent mode - set your preferred drag&drop action and bypass the gui
#        ask for vaperture (for cameras) - prompts for a vertical aperture if a camera chan file is dropped
#        use ReadGeoPlus gizmo instead of default ReadGeo - only us if ReadGeoPlus is installed in your Nuke environment
#
# To set up preferences do the following:
#
# create ~/.nuke/drop.preference and put the following lines into it:
# mode {<mode>}
# va_prompt <switch>
# ReadGeoPlus <switch>
#
# the following modes are supported:
# as sequence - always import subsequent frames as a sequence (singe Read/ReadGeo node)
# as stills - always create one Read/ReadGeo node for each file
# only folders as sequence - only sequences within a folder are read into a single Read/ReadGeo node
# always prompt - always ask the user every time a sequence is found
#
# example:
# mode {only folders as sequence}
# va_prompt 1
# ReadGeoPlus 1
#
# update Sept/22/2006
#    -fixed problem with large number of files
# update Nov/13/2006
#    -fixed assignment of string and frame range in 4.5.27
# update Jul/31/2007
#    -added support for nuke file syntax (i.e. %04d etc.) since this is now also called for copy/pasting stuff
# update Sep/12/2007
#    -fixed problem with white space in file name. make sure to use compressList2 with this version
############################################################################################
proc testChan {inputfile} {
   set chan [open $inputfile r]
     while {[gets $chan line] >= 0} {
       if {[llength $line] < 4} continue
       if {[llength $line] == 8} {
           close $chan
           return 1
           } elseif {[llength $line] == 7} {
               close $chan
               return 0
               }
       }
   }
############################################################################################
proc getPrefs {} {
   set chan [open ~/.nuke/drop.preference r]
   set validModes {0 {as sequence} {as stills} {only folders as sequence} {always prompt}}
   set compress 0
   set va_prompt 0
   set geoPlus 0
   while {[gets $chan line] > -1} {
       regexp {(^mode\s+){?([\w\s]+)}?} $line mgarbage vmode compress
       regexp {(^va_prompt\s+){?(\d)}?} $line agarbage amode va_prompt
       regexp {(^ReadGeoPlus\s+){?(\d)}?} $line rgarbage rmode geoPlus
       }
   close $chan

   if [info exists compress] {
       if {[lsearch $validModes $compress] == -1} {
           message "skipping unkown compress mode in:\n\"$mgarbage\"\nin\n[getenv HOME]/.nuke/drop.preference\n\nSupported modes:\n[join [lrange $validModes 1 end] "\n"]"
           set compress 0
           }
       }


   return [list $compress $va_prompt $geoPlus]
   }
############################################################################################
proc drop {text} {
   set supportedImg {.jpg .jpeg .tif .tiff .tif16 .tiff16  .ftif .ftiff .exr .hdr .tga .gif .cin .dpx .png .png16 .targa .iff .sgi .sgi16 .rgb .rgba .xpm .pic .yuv}
   #if "~/.nuke/drop.preference"  exists, set behavior and bypass UI
   if [file exists "[getenv HOME]/.nuke/drop.preference"] {
       set prefs [getPrefs]
       set compress [lindex $prefs 0]
       set va_prompt [lindex $prefs 1]
       set geoPlus [lindex $prefs 2]
       } else {
           set compress 0
           set va_prompt 0
           set geoPlus 0
           }
      array set singleFiles {}
   set singleFileList {}
   set incomingText [split $text "\r\n"]

   foreach raw_line $incomingText {

       #clean up the input list and append directory content
       set raw_line [string trim $raw_line]
       if {$raw_line=={}} continue
       # strip the Linux 'file:' prefix
       if [string match "file:*" $raw_line] {
           set raw_line [string range $raw_line 5 end]
           }
       # strip Linux '///' to '/'
       if [string match "///*" $raw_line] {
           set raw_line [string range $raw_line 2 end]
           }
       #append directory content
       if [file isdirectory $raw_line] {
           set singleFileList [concat $singleFileList [glob $raw_line/*]]
           } else {
               #anything else but directories
               if [regexp {%\d+d} $raw_line] {
                   #expand nuke syntax into file list
                   set singleFileList [concat $singleFileList [expandList $raw_line]]
                   } else {
                       #single file
                       lappend singleFileList $raw_line
                       }
               }
       #expand and append conpressed lists
       }


   foreach cur_line $singleFileList {
       ################
       #create cameras, axes and add nuke scripts
       #collect files for Read and ReadGeo nodes
       switch [file extension $cur_line] {

           ".nk" - ;".nk3" - ;".nk4" - ;".nuke" - ;".nuke3" - ;".nuke4" - ;".autosave" {
               #bring in Nuke scripts
               puts " pasting nuke file\n$text"
               source $cur_line
               }
           ".obj" {
               #collect data for obj files
               if $geoPlus {
                   lappend singleFiles(ReadGeoPlus) "\"$cur_line\""
                   } else {
                   lappend singleFiles(ReadGeo) "\"$cur_line\""
                   }
               }
           ".chan" {
               #bring in chan files
	       if [testChan $cur_line] {
                   puts " pasting camera chan file\n$text"
                   push 0
                   Camera -New
                   set newNode [stack 0]
                   knob $newNode.selected 0
                   if {$va_prompt == 1} {
                       set va [value $newNode.vaperture]
                       if [catch {panel "Track Camera" {{"Vertical Aperture" va}}}] {
                           delete $newNode
                           return
                           }
                       knob $newNode.vaperture $va
                       }
                   } else {
                       puts " pasting axis chan file\n$text"
                       push 0
                       Axis {}
                       set newNode [stack 0]
                       knob $newNode.selected 0
                       }
               in $newNode {import_chan_file $cur_line}
               }
           default {
               #check if Nuke likes the remaining file
		if {[lsearch $supportedImg [file extension $cur_line]] >= 0} {
                       lappend singleFiles(Read) "\"$cur_line\""
                       }

               }
           }
              }

   foreach curClass [array names singleFiles] {
       ################
       #create compressed lists according to user input
       puts "comparing:\n\t[lsort $singleFiles($curClass)]\n\t[lsort [compressList2 $singleFiles($curClass)]]"
       if {[llength $singleFiles($curClass)]  != [llength [compressList2 $singleFiles($curClass)]]} {
           if {$compress == 0} {
                   #if there are files that could be compressed ask the user
                   set name [basename [lindex [compressList2 $singleFiles($curClass)] 0]]
                   if [catch {panel "Sequence handling" {
                   {"import subsequent frames" compress e {"as sequence" "as stills" "only folders as sequence" "always prompt"}}
                   }}] {return}
                   }
           switch $compress {
               "as sequence" {
                   set readyToPaste [compressList2 $singleFiles($curClass)]
                   }
               "as stills" {
                   set readyToPaste $singleFiles($curClass)
                   }
               "only folders as sequence" {
                   set readyToPaste {}
                   set folderSeq {}
                   foreach curItem $singleFiles($curClass) {
                       if {[lsearch $incomingText [file dirname $curItem]] > -1} {
                           lappend folderSeq $curItem
                           } else {
                               lappend readyToPaste $curItem
                               }
                       }
                   set readyToPaste [concat $readyToPaste [compressList2 $folderSeq]]
                   }
               "always prompt" {
                   foreach curItem [compressList2 $singleFiles($curClass)] {
                           if {[lsearch $incomingText $curItem] < 0} {
                               set promptWidth [expr [string length $curItem]*7]
                               if [catch {panel -w$promptWidth $curItem {
                                   {"import as " compressPrompt e {"sequence" "stills"}}
                                   }}] {return}
                           if {$compressPrompt == "sequence"} {
                               lappend readyToPaste $curItem
                               } else {
                                   set first [lindex [split [lindex $curItem 1] "-"] 0]
                                   set last [lindex [split [lindex $curItem 1] "-"] 1]
                                   for {set i $first} {$i <= $last} {incr i} {
                                       lappend readyToPaste [format [lindex $curItem 0] $i]
                                       }
                                   }
                               } else {
                                   lappend readyToPaste $curItem
                                   }

                           }
                   }
               }
           } else {
               #no sequences, just pull in stills
               set readyToPaste $singleFiles($curClass)
               }
       foreach pasteItem $readyToPaste {
           #create Read or GeoRead nodes
           puts " pasting $curClass node \n$pasteItem"
           push 0
           $curClass -New
           knob [stack 0].selected 0
           in [stack 0] {
               knob file [lindex $pasteItem 0]
               catch {knob first [lindex [split [lindex $pasteItem 1] "-"] 0]}
               catch {knob last [lindex [split [lindex $pasteItem 1] "-"] 1]}
               }
           }
       }
   }


