#####################
#written by Frank Rueter
#last modified	Aug/22/2006
#this is creates and extra tab in a Bezier node.
#It needs BezierGeoProc.tcl to create geometric shapes with a Bezier node
#the following shapes are supported: circle, oval, square, rectangle, triangle.
#circle and square take into account the input's pixel aspect while oval, rectangle and triangle
#are absolute
#####################
proc BezierGeoTab {} {
	set curNode [stack 0]
	if {[class $curNode] != "Bezier"} {
		message "Select a Bezier node first"
		return
		}
	addUserKnob node $curNode 20 "" Geo
	addUserKnob node $curNode 4 type label "type" M {"circle" "square" "oval" "rectangle" "triangle"} t "set the shape of the bezier"
	addUserKnob node $curNode 32 "" label "set" T "BezierGeoProc \[knob this.type]" t "sets the shape of this bezier to what is set in 'type'"
}
