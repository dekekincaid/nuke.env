#written by frankr
#last update 21.02.2006
###################
# mirrors the selected nodes' position in the DAG for easy rearranging
###################

proc MirrorNodePos {axis} {

array set nodePos {}
set xTotal 0
set yTotal 0
foreach cur_node [selected_nodes] {
	set xTotal [expr $xTotal+[knob $cur_node.xpos]]
	if [knob $cur_node.postage_stamp] {
		lappend nodePos($cur_node) [knob $cur_node.xpos] [expr [knob $cur_node.ypos] + 21]
		set yTotal [expr $yTotal+[expr [knob $cur_node.ypos] + 21]]
		} else {
		lappend nodePos($cur_node) [knob $cur_node.xpos] [knob $cur_node.ypos]
		set yTotal [expr $yTotal+[knob $cur_node.ypos]]
		}
	}
set xAxis [expr $xTotal/[llength [selected_nodes]]]
set yAxis [expr $yTotal/[llength [selected_nodes]]]

foreach cur_node [array name nodePos] {
	if {[string tolower $axis] == "x"} {
		knob $cur_node.xpos [expr [knob $cur_node.xpos] - ([lindex $nodePos($cur_node) 0]-$xAxis)*2]
		} elseif {[string tolower $axis] == "y"} {
		knob $cur_node.ypos [expr [knob $cur_node.ypos] - ([lindex $nodePos($cur_node) 1]-$yAxis)*2]			
		}
	}

}