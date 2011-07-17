#####################
#written by Franke Rueter
#last modified Apr/13/2006
#		Nov/27/2007 -	using card's z knob instead of extra TransfromGeo node
#				adding switch for LatLong output
#this is used by Projector.gizmo
#####################

proc createProjectorEnv {} {
#	source /job/COMMON/lib/nuke/user-gizmos/frueter/rangeToListSimple.tcl
	set counter 1
	set NewNodes {}
	in this {
		#delete existing nodes
		foreach cur_node [nodes] {
			if {[knob $cur_node.label] == "auto generated"} {
				delete $cur_node
				}
			}
		foreach cur_frame [rangeToListSimple [knob this.range]] {
			##FrameHold node
			push IMG
			FrameHold {}
			set curNode [stack 0]
			knob $curNode.label "auto generated"
			knob $curNode.first_frame $cur_frame
			lappend NewNodes $curNode
			##Card node
			Card {}
			set curNode [stack 0]
			knob $curNode.label "auto generated"
			knob $curNode.lens_in_focal "parent.use_input?CAM_EXT.focal($cur_frame):CAM_ANIM.focal($cur_frame)"
			knob $curNode.lens_in_haperture "parent.use_input?CAM_EXT.haperture($cur_frame):CAM_ANIM.haperture($cur_frame)"
			knob $curNode.z "parent.distance"
			knob $curNode.selectable 0
			lappend NewNodes $curNode
			##TransformGeo node
			TransformGeo {}
			set curNode [stack 0]
			knob $curNode.label "auto generated"
			in $curNode.translate.x {set_expression "parent.use_input?CAM_EXT.translate.x($cur_frame):CAM_ANIM.translate.x($cur_frame)"}
			in $curNode.translate.y {set_expression "parent.use_input?CAM_EXT.translate.y($cur_frame):CAM_ANIM.translate.y($cur_frame)"}
			in $curNode.translate.z {set_expression "parent.use_input?CAM_EXT.translate.z($cur_frame):CAM_ANIM.translate.z($cur_frame)"}
			in $curNode.rotate.x {set_expression "parent.use_input?CAM_EXT.rotate.x($cur_frame):CAM_ANIM.rotate.x($cur_frame)"}
			in $curNode.rotate.y {set_expression "parent.use_input?CAM_EXT.rotate.y($cur_frame):CAM_ANIM.rotate.y($cur_frame)"}
			in $curNode.rotate.z {set_expression "parent.use_input?CAM_EXT.rotate.z($cur_frame):CAM_ANIM.rotate.z($cur_frame)"}
			knob $curNode.selectable 0
			lappend NewNodes $curNode
			##END OF NODE GENERATION
			input MasterScene $counter $curNode
			incr counter
		}
	eval [concat autoplace $NewNodes]
	
	}
}
