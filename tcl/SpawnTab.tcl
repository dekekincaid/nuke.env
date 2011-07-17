#written by frank rueter
#adds a tab to the Tracker node to generate linked nodes
proc SpawnTab {} {
	set curNode [stack 0]
	if {[class $curNode] != "Tracker"} {
		message "Select a tracker node first"
		return
		}
	addUserKnob node $curNode 20 "" Spawn
	addUserKnob node $curNode 4 linkToPos label "position" M { "tracker" "offset tracker" "average 1,2" "average 1,2,3" "average 3,4" "average 1-4" }
 	addUserKnob node $curNode 4 reference label "reference" M { "absolute" "use ref frame" }
	addUserKnob node $curNode 26 "" ""
	addUserKnob node $curNode 6 use_pos label "use position"
 	addUserKnob node $curNode 6 use_rot label "use rotation"
 	addUserKnob node $curNode 6 use_scale label "use scale"
	addUserKnob node $curNode 35 newNode label "generate node" M {
		Bezier "
		set usedXforms {}
		lappend usedXforms [knob use_pos] [value use_rot] [value use_scale]
		SpawnNode Bezier [value linkToPos] $usedXforms [value reference]
		"
		Transform "
		set usedXforms {}
		lappend usedXforms [knob use_pos] [value use_rot] [value use_scale]
		SpawnNode Transform [value linkToPos] $usedXforms [value reference]
		"
		Position "SpawnNode Position [value linkToPos] {1 0 0} [value reference]"
		CornerPin "SpawnNode CornerPin [value linkToPos] {1 1 1} [value reference]"
		}
	knob $curNode.use_pos 1
}
