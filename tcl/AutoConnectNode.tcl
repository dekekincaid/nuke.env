######  
# by frankr@wetafx.co.nz
# creates nodes with multiple inputs (depending on argument) and auto connects all selected nodes to it.
# last modified:
#	09.01.2006
#	20.01.2006  - 	added feature to connect nodes according to their horizontal order in the DAG (left most node is input 0)
#			added Weta tab to update the input order for existing connections
###### 


proc reconnectInputs {} {
if [info exists cur_inputs] {unset cur_inputs}
#collect existing inputs
for {set in 0} {$in <= [expr [inputs this]-1] } {incr in} {
	if {[input this $in] != 0} {
		lappend cur_inputs [input this $in]
		input this $in 0
		}
}

if ![info exists cur_inputs] {puts "no inputs connected"; return}

#sort inputs by x position
array unset nodePos
array set nodePos {}
foreach cur_node $cur_inputs {
	set nodePos([knob $cur_node.xpos]) $cur_node
	}

#reconnect input nodes
if [info exists cur_pipe] {unset cur_pipe}
set cur_pipe 0
foreach key [lsort -real [array names nodePos]] {
	puts "connecting [knob $nodePos($key).name] with position $key"
	input this $cur_pipe $nodePos($key)
	incr cur_pipe
	}

}



proc AutoConnectNode {nodeType} {


if {[catch {set cur_nodes [selected_nodes]}]} {
	$nodeType -New {}
	} else {
	array set nodePos {}
	foreach cur_node [selected_nodes] {
		set nodePos([knob $cur_node.xpos]) $cur_node
		}
	
	$nodeType -New {}
	set newNode [stack 0]
	set cur_pipe 0
	
	foreach key [lsort -real [array names nodePos]] {
		if {[class $nodePos($key)] != "BackdropNode"} {
			puts "connecting [knob $nodePos($key).name] with position $key"
			input $newNode $cur_pipe $nodePos($key)
			incr cur_pipe
			}
		}
 addUserKnob node $newNode 20 "" Weta
 addUserKnob node $newNode 32 "update input order" T " reconnectInputs" t "changes the input order according to the input nodes' horizontal order (left most node becomes input 0)"

	}
if {$nodeType == "ContactSheet"}  {
	knob $newNode.width 2048
	knob $newNode.height 1157
	knob $newNode.columns 4
	knob $newNode.rows [expr ceil($cur_pipe / 4.0) ]
	}

}
