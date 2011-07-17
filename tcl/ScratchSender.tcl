# code by throb
# works like this 
# ScratchSender \\path\\to\\place\\footage\\ Project Group Construct
# ScratchSender \\\\swaydi\\array\\redcarpet\\renders\\RC080\\RC80TEST RedCarpet Renders Import
# please note the double \ needed for escaping the \ character
# the script will create the directory so be sure that the path is correct in your menu.tcl file
# sample menu.tcl info
# menu "JOB/RedCarpet/Send to Scratch" {ScratchSender \\\\swaydi\\array\\redcarpet\\renders RedCarpet Renders Import}

proc ScratchSender args {

global env
global shot

# use this to tell the script where scratch looks for its xml data
set watchdir "z:/job/scratch"

if {[class [selected_node]] != "Read" && [class [selected_node]] != "Write"} {
	error "Please select a Read or Write node"
	break
}

if  {[class [selected_node]] == "Read"} {
			set startframe [knob [selected_node].first]
			set endframe [knob [selected_node].last]
			
} else {

	set startframe [knob root.first_frame]
	set endframe [knob root.last_frame]
}
	
		set xmlfile [file tail [filename [selected_node]]]
		set xmlfile [string range $xmlfile 0 [expr [string length $xmlfile]-10]]
		puts "Sending : $xmlfile"
	
			regsub "\.nk" $xmlfile "" xmlfile
			
			set shotend [string first _ $xmlfile]
      set shot [string range $xmlfile 0 [expr $shotend-1]] 
	
	set path [lindex $args 0]\\$shot
	set project [lindex $args 1]
	set group [lindex $args 2]
	set desk [lindex $args 3]
	set sender $env(USERNAME)
	set date [clock format [clock seconds] -format "%a %m-%d-%y %T"]

if {![file isdirectory $path]} {
file mkdir $path\\$xmlfile
}



set initstartframe $startframe
set initendframe $endframe
	
if ![catch {
		panel -w300 "Send to Scratch 1.1" {
			{"Start Frame" startframe}
      {"End Frame" endframe}
		}
	}] {

		
			set sourcefile [filename [selected_node]]
			regsub -all "/" $sourcefile "\\" sourcefile

			set endframe [format "%d" $endframe]
			set sourcestartframe [format "%04d" $startframe]
			
			regsub "\%04d" $sourcefile $sourcestartframe sourcefile
			
			set startframe [format "%d" $startframe]
			set startframe [expr abs ($initstartframe-$startframe)]
			set endframe [expr $endframe-$startframe]
			
			set openfile "z:/job/scratch/archive/$xmlfile.xml"
			
			set fileid [open $openfile w]
			
			# create the XML
						
			puts $fileid "<?xml version=\"1.0\"?>"
			puts $fileid "<commands>"
			puts $fileid "		<result file=\"\\\\swaydi\\array\\$project\\resultfile.txt\"></result>"
			puts $fileid "		<log file=\"\\\\swaydi\\array\\$project\\logfile.txt\"></log>"
			puts $fileid "		<command name=\"LOAD\">"
			puts $fileid "			<!-- source is where it grabs data -->"
			puts $fileid "			<source>$sourcefile</source>"
			puts $fileid "			<!-- path is output path -->"
			puts $fileid "			<path>$path\\$xmlfile</path>"
			puts $fileid "			<range>0,$endframe</range>"
			puts $fileid "			<project>$project</project>"
			#puts $fileid "			<group>$show</group>"
			puts $fileid "			<group>$group</group>"
			puts $fileid "			<desk>$desk</desk>"
      # one day i will deal with the edit stuff here but i am too lazy right now
			#puts $fileid "			<!--<reel> 1 | first | last </reel> -->"
			puts $fileid "      <reel>last</reel>"
			puts $fileid "			<layer>0</layer>"
			puts $fileid "			<clipname>$xmlfile</clipname>"
			puts $fileid "			<note>\"$shot Sent By : $sender on $date\"</note>"
			puts $fileid "		</command>"
			puts $fileid "</commands>"
			
			close $fileid
			
			file copy -force $openfile $watchdir/$xmlfile.xml
	}
}
