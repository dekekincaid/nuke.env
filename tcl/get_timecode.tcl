# DPX - Nuke Timecode Render
#(C) MinselProductions
# martin91573@aol.com
#
#
#This Nuke - script writes a timecode-information to your rendered dpx files 
#1. copy this file to your Nuke/plugins folder
#2. open the menu.tcl in the same folder and add at the end of the file "load get_timecode.tcl"
#3. open your composition in Nuke
#4. change the filetype to dpx 
#5. type in the timecode textfield: [get_timecode {X}]
#	X is your desired Timecodeoffset. (if you do not want to have an Offset then X=1)
#6. press "execute"
#

proc get_timecode {customstart} {
	set start [knob root.first_frame]
	set end [knob root.last_frame]
	set actFrame [knob root.frame]
	set actualframe [knob root.frame]
	set framenumber [expression $end-$start]
	set sec [knob root.fps]
	set hour [expr $sec*360]
	set min [expr $sec*60]
	

	#set customstart [get_input "Custom Time Offset:" ]
	
		set actualframe [expr $actFrame + ($customstart-1)]
				set out [expr $actualframe]
		set th [expr floor(($actualframe/$hour))]
		set actualframe [expr $actualframe - ($th*$hour)]
			set th [format "%.0f" $th]
			set th [format "%02d" $th]
			set help ${th}
		set tm [expr floor(($actualframe/$min))]
		set actualframe [expr $actualframe - ($tm*$min)]
			set tm [format "%.0f" $tm]
			set tm [format "%02d" $tm]
			set help ${help}${tm}
		set ts [expr floor(($actualframe/$sec))]
		set actualframe [expr $actualframe - ($ts*$sec)]
			set ts [format "%.0f" $ts]
			set ts [format "%02d" $ts]
			set help ${help}${ts}
		for {set x 0} {$x<$actualframe+1} {incr x} {
			set tf [expr $x]
		}
			set tf [format "%02d" $tf]
			set help ${help}${tf}
}