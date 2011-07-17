#written by frank rueter
#generates nodes that are linked to the tracker.
#needed for SpawnTab.tcl
proc SpawnNode {NewNode sourceKnob Xform ref} {
	knob this.selected 0
	push 0
	set TrackerName [value this.name]
	set refFrame "$TrackerName.refframe"
	#get source position
	switch $sourceKnob {
		"tracker" {set XformKnob "tracker1"}
		"offset tracker" {set XformKnob "tracker1off"}
		"average 1,2" {set XformKnob "avg12"}
		"average 1,2,3" {set XformKnob "avg123"}
		"average 3,4" {set XformKnob "avg34"}
		"average 1-4" {set XformKnob "avg1234"}
		}
	#create expressions
	if {$ref == "absolute"} {
		set translateX "{$TrackerName.$XformKnob.x} {$TrackerName.$XformKnob.y}"
		set rotateX "{$TrackerName.rot12}"
		set scaleX "{$TrackerName.scale12}"
		} else {
		set translateX "{$TrackerName.$XformKnob.x-$TrackerName.$XformKnob.x($refFrame)} {$TrackerName.$XformKnob.y-$TrackerName.$XformKnob.y($refFrame)}"
		set rotateX "{$TrackerName.rot12-$TrackerName.rot12($refFrame)}"
		set scaleX "{$TrackerName.scale12-$TrackerName.scale12($refFrame)}"		
		}
	#generate linked nodes
	switch $NewNode {
		Bezier {
			Bezier
			set CurNode [stack 0]
			if [lindex $Xform 0] {knob $CurNode.translate $translateX}
			if [lindex $Xform 1] {knob $CurNode.rotate $rotateX}
			if [lindex $Xform 2] {knob $CurNode.scale $scaleX}
			}
		Transform {
			Transform
			set CurNode [stack 0]
			if [lindex $Xform 0] {knob $CurNode.translate $translateX}
			if [lindex $Xform 1] {knob $CurNode.rotate $rotateX}
			if [lindex $Xform 2] {knob $CurNode.scale $scaleX}
			}
		Position {
			Position
			set CurNode [stack 0]
			knob $CurNode.translate $translateX
			}
		CornerPin {
			CornerPin2D
			set CurNode [stack 0]
			if {$ref == "absolute"} {
				knob $CurNode.to1 "{$TrackerName.tracker1.x} {$TrackerName.tracker1.y}"
				knob $CurNode.to2 "{$TrackerName.tracker2.x} {$TrackerName.tracker2.y}"
				knob $CurNode.to3 "{$TrackerName.tracker3.x} {$TrackerName.tracker3.y}"
				knob $CurNode.to4 "{$TrackerName.tracker4.x} {$TrackerName.tracker4.y}"
				} else {
				knob $CurNode.to1 "{$TrackerName.tracker1.x-$TrackerName.tracker1.x($refFrame)} {$TrackerName.tracker1.y-$TrackerName.tracker1.y($refFrame)}"
				knob $CurNode.to2 "{$TrackerName.tracker2.x-$TrackerName.tracker2.x($refFrame)} {$TrackerName.tracker2.y-$TrackerName.tracker2.y($refFrame)}"
				knob $CurNode.to3 "{$TrackerName.tracker3.x-$TrackerName.tracker3.x($refFrame)} {$TrackerName.tracker3.y-$TrackerName.tracker3.y($refFrame)}"
				knob $CurNode.to4 "{$TrackerName.tracker4.x-$TrackerName.tracker4.x($refFrame)} {$TrackerName.tracker4.y-$TrackerName.tracker4.y($refFrame)}"
				}
			}
		}
	}
