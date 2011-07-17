#
# Connect2Tracker 2007-08 demOOn.k@gmail.com
# ver 0.3
#
# Exmaple of use:
# Connect to Ctrl T: Add to menu.tcl
# menu "Transform/Connect2tracker" "^t" Connect2Tracker
# Thanx DenizZ, Ali
#


proc Average {infun num} {
	set sum 0
	for {set i 0} {$i<$num} {incr i} {
	 set sum [expr $sum+[value "${infun}(t+$i)"]]
	}
	return [expr $sum/$num]
}

########## added by ali ###########################################################################
#Sort points from left bottom by counterclockwise (2,3 or 4 points required)
#point_list - for example {{x0 y0} {x1 y1} {x2 y2} {x3 y3}}
#function return list of sorted indexes - for example {1 0 3 2}
proc SortForCornerPin {points_list} {
	if {[llength $points_list]<2 || [llength $points_list]>4} {return 0}
	#create list {{x0 y0 0} {x1 y1 1} {x2 y2 2} {x3 y3 3}}
	set i 0
	set plist {}
	foreach xy $points_list {
		lappend plist [concat $xy $i]
		incr i
	}
	
	#sort list 
	set plist [lsort -real -index 1 $plist]
	if {[llength $points_list]==4} {
		set plist [concat [lsort -real -index 0 [lrange $plist 0 1]] [lsort -decreasing -real -index 0 [lrange $plist 2 3]]]
	} elseif {[llength $points_list]==3} {
		set plist [concat [lsort -real -index 0 [lrange $plist 0 1]] [list [lindex $plist 2]]]
	}
	
	#make list of sorted indexes
	set indexes {}
	foreach item $plist {
		lappend indexes [lindex $item end]
	}
	return $indexes
}
##################################################################################################

proc Connect2Tracker {} {

########## added by ali ###########################################################################
#Sort nodes in order:  Position, Tracker, all other nodes...
	set sel_nodes {}
	foreach n [selected_nodes] {
		if {[class $n] == "Position"} {lappend sel_nodes $n}
		#Use not more than 4 Position nodes
		if {[llength $sel_nodes]>=4} break
	}
	#Sort Position nodes by transform values for using with CornerPin...
	if {[llength $sel_nodes]>1} {
		#create list {{x0 y0} {x1 y1} {x2 y2} {x3 y3}} from Position nodes "translate" values
		foreach n $sel_nodes {lappend plist [value $n.translate]}
		#sort list 
		set indexes [SortForCornerPin $plist]
		#sort nodes
		set tmp_nodes {}
		foreach index $indexes {lappend tmp_nodes [lindex $sel_nodes $index]}
		set sel_nodes $tmp_nodes

	}
	
	foreach n [selected_nodes] {if {[class $n] == "Tracker3"} {lappend sel_nodes $n} }
	foreach n [selected_nodes] {if {[class $n] != "Tracker3" && [class $n] != "Position"} {lappend sel_nodes $n} }
##################################################################################################

#find a tracker
	set trk_nodes 0
	set pos_nodes 0
	set cst_nodes 0
	
	foreach sel_node $sel_nodes {
		if {[class $sel_node] == "Tracker3"} {
			incr trk_nodes
			set TrackNode [full_name [value $sel_node.name]]
		}
		if {[class $sel_node] == "Position"} {
			incr pos_nodes
			set PosNode($pos_nodes) [full_name [value $sel_node.name]]
		}
		if {[class $sel_node] == "Transform" && [exists $sel_node.ManageTrackers]} {
			incr trk_nodes
			set TrackNode [full_name [value $sel_node.name]]
		}
	}
	if {$trk_nodes != 1 && $pos_nodes == 0} {alert "Please select one tracker or position"; return}
# connecting if tracknode exists
	if {$trk_nodes == 1} {
		set curtrack 0
		foreach sel_node $sel_nodes {

			set sel_node [full_name [value $sel_node.name]]
			switch -- [class $sel_node] {
				"Position" {
					incr curtrack
					if {$curtrack < 5} {
						knob $TrackNode.enable$curtrack 1
						knob $TrackNode.use_for$curtrack 7
						knob $TrackNode.track$curtrack "[knob $sel_node.translate]"
					}
				}
				"Bezier" - "Transform" - "TransformMasked" {
					knob $sel_node.translate "[value $TrackNode.name].translate.x [value $TrackNode.name].translate.y"
					knob $sel_node.center "[value $TrackNode.name].center.x [value $TrackNode.name].center.y"
					knob $sel_node.rotate "[value $TrackNode.name].rotate"
					knob $sel_node.scale "[value $TrackNode.name].scale"
				}
				"CornerPin2D" {
					#create list {{x0 y0} {x1 y1} {x2 y2} {x3 y3}} from Position nodes "translate" values
					set plist {}
					for {set i 1} {$i<5} {incr i} {
						if {[value $TrackNode.enable$i]} {lappend plist [value $TrackNode.track$i]}
					}
					#sort list
					set indexes [SortForCornerPin $plist]
					#connect CornerPin to Tracker
					set i 1
					foreach index $indexes {
						incr index
						knob "$sel_node.to$i" "[value $TrackNode.name].track$index.x [value $TrackNode.name].track$index.y"
						knob "$sel_node.enable$i" "[value [value $TrackNode.name].enable$index]"
						
						#For copy in CornerPin values from "to" to "from" uncoment next string
						#knob "$sel_node.from$i" [value "$sel_node.to$i"]
						incr i
					}
				}
				default {
				}
			}
		}
		if {($curtrack > 0) && ($curtrack < 5)} {
			for {set i 4} {$i > $curtrack} {incr i -1} {
			knob $TrackNode.enable$i 0
			knob $TrackNode.use_for$i 0
			}
		}
	} else {
	# only position nodes
		push [node root]
		Transform {}
		set TrackNode [stack 0]
		knob $TrackNode.name "Tracker[value $TrackNode.name]"
		addUserKnob [list node $TrackNode 20 "" l ManageTrackers]
		addUserKnob [list node $TrackNode 3 ReferenceFrame]
		knob $TrackNode.ReferenceFrame [value frame]
		addUserKnob [list node $TrackNode 32 "" l "Set to current" T "knob this.ReferenceFrame \[value frame]"]
		addUserKnob [list node $TrackNode 20 "" l "Smooth frames" n 1]
		addUserKnob [list node $TrackNode 3 T]
		addUserKnob [list node $TrackNode 3 R]
		addUserKnob [list node $TrackNode 3 S]
		addUserKnob [list node $TrackNode 3 C]
		addUserKnob [list node $TrackNode 20 endGroup n -1]
		
		set curtrack 0
		foreach sel_node [selected_nodes] {

			set sel_node [full_name [value $sel_node.name]]
			switch -- [class $sel_node] {
				"Position" {
					incr curtrack
					addUserKnob [list node $TrackNode 12 Track$curtrack ]
					knob $TrackNode.Track$curtrack "[knob $sel_node.translate.x] [knob $sel_node.translate.y]"
					addUserKnob [list node $TrackNode 6 t$curtrack  l T]
					knob $TrackNode.t$curtrack  true
					addUserKnob [list node $TrackNode 6 r$curtrack  l R]
					knob $TrackNode.r$curtrack  true
					addUserKnob [list node $TrackNode 6 s$curtrack  l S]
					knob $TrackNode.s$curtrack  true
					addUserKnob [list node $TrackNode 6 c$curtrack  l C]
					knob $TrackNode.c$curtrack  true
				}

				default {
				}
			}
		}
		if {$curtrack > 1} {
			set sum_t "t1"
			set sum_c "c1"
			set sum_tr "Track1"
			
			for {set i 2} {$i <= $curtrack} {incr i} {
				set sum_t "$sum_t+t$i"
				set sum_tr "$sum_tr+Track$i"
				

			}
			
# 							 (t1+t2)?(t1*(Track1.x - Track1.x(1)) + t2*(Track2.x - Track2.x(1)))/(t1+t2):width/2

			knob $TrackNode.center "($sum_t)?(($sum_tr)/($sum_t)):0 ($sum_t)?(($sum_tr)/($sum_t)):0"

		}
	}


}