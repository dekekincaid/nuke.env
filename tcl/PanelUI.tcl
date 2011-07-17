proc ColorDemo {} {			
	for {set i 0} {$i < 256} {incr i} {
		Dot "
		xpos [expr fmod($i,16)*80]
		ypos [expr (ceil($i/16))*70]
		tile_color $i
		name \"tile_color\"
		label $i
		"
		push 0
		}
}
#proc to open the code
proc openCode {} {
	#find the location this file is saved in
	foreach cur_plugin [plugins] {
		if {[basename $cur_plugin] == "PanelUI.tcl"} {set input $cur_plugin;break}
		}
	#rea the tcl file
	set newText ""
	set chan [open $input r]
	set lineNumber 0
	while {[gets $chan line] >= 0} {
		append newText $line\n
		}
	close $chan
	#pop up panel with code in it
	if [catch {panel -w900 "code for Panel UI Demo" {{"" newText n67}}}] {return}
}
#proc to do the panel ui stuff
proc PanelUI {} {
	#get environment variables
	global env
	#set default values for widgets
	if [info exists env(USERNAME)] {set inputFile "/job/HOME/$env(USERNAME)/.nuke/"}
	if [info exists env(TEMP)] {set inputImage "$env(TEMP)"}
	set inputTextOne "single line text"
	set inputTextSmall "I got lots more space\nto write stuff in here.\nJust about three lines"
	set inputTextBig "This is a larger multiline input\nso you can write even more.\nSince I can't think of anything\n to put into all these lines\nI'll just shut up"
	set inputTextHuge "the number of this notepad is actually customizable.\nYou get the idea..."
	set checkBox 0
	set rgbColor 14
	set pulldown item2
	set xInput {1+2}
	#build the panel
	if [catch {panel -w500 "Panel UI Demo" {
		{"file browser: " inputFile f}
		{"image browser: " inputImage f2}
		{"@B10;text input singe line" inputTextOne}
		{"@B11;text input small" inputTextSmall m}
		{"@B12;text input large" inputTextBig m2}
		{"@B13;notepad with\ncustomizable number\nof lines" inputTextHuge n6}
		{"rgb color chip" rgbColor c}
		{"pulldown menu" pulldown e {item1 item2 item3 item4 item5}}
		{"text font pulldown menu" pulldownFont F}
		{"expression input" xInput x}
		{"show available tile colors" checkBox b}
		}}] {
		message {panel cancelled}
		} else {
		if $checkBox {
			ColorDemo
			}
		if [ask "open the code?"] {openCode}
		}
}
