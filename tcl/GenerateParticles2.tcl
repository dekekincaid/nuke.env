#####################
#written by Frank Rueter
#last modified	 Apr/20/2006
#		  Apr/21/2006 - added per particle variations for size, speed and spread
#		  Apr/24/2006 - added "inherit velocity" functionality
#		  Apr/25/2006 - added preset functionality
#		  Aug/29/2007 - dynamic scene node generation to increae the limit to 999*999 particles
#		  		added support for animated textures
#		  		cards now obey the resolution knob
#		  		
#		  		
#this is used by Particles.gizmo
# needs /job/COMMON/lib/nuke/user-gizmos/frueter/ObjVPos.tcl
# needs /job/COMMON/lib/nuke/user-gizmos/frueter/SaveParticlePresets.tcl
# needs /job/COMMON/lib/nuke/user-gizmos/frueter/LoadParticlePresets.tcl
#####################

proc GenerateParticles2 {geoMode} {
######################### SUB PROC
	proc getObjInfo {geoMode} {
		# GET SOURCE POSITIONS
		if {[class this.input0] == "ReadGeo"} {
			if {![file exists [value this.input0.file]]} {
				message "No file found:\n[value this.input0.file]\nin [value this.input0.name]"
				return
				}
			set emitterFile [value this.input0.file]
			set sourceList [ObjVPos $emitterFile $geoMode]
			} else {
			puts "\nWriting emitter geo to:\n[value WriteEmitter.file]"
			execute WriteEmitter [expression rint([value frame])]
			set emitterFile [value WriteEmitter.file]
			set sourceList [ObjVPos $emitterFile $geoMode]
#			file delete $emitterFile
			}
		return $sourceList
		}

######################### SUB PROC END


	in this {
		# DELETE EXISTING NODES
		foreach cur_node [nodes] {
			if {[knob $cur_node.label] == "auto generated"} {
				delete $cur_node
				}
			}

		# CHECK WHICH IMG PIPES ARE CONNECTED
		for {set i 1} {$i<=5} {incr i} {
			set imgIn "img$i"
			set imgInputs($imgIn) "input[value $imgIn.number]"
			}
		foreach cur_pipe [array names imgInputs] {
			if [exists this.$imgInputs($cur_pipe)] {set connectedInputs($cur_pipe) $imgInputs($cur_pipe)}
			}


		if {[class this.input1] != "Axis" && [exists this.input1]} {
			puts "surface emitter"
			set emissionPoints [getObjInfo [string index [value emitter_mode] 0]]
			} else {
			puts "point emitter"
			set emissionPoints {{0 0 0}}
			}

		 #################################################################################
		 #generate new nodes #############################################################
		 #################################################################################
		puts "starting node generation"
		set counter 1
		set NewNodes {}
		set ReadNodes {}
		foreach cur_imgIn [array names connectedInputs] {
			push $cur_imgIn
			Reformat "
					to_format false
					to_scale true
					scale parent.pre_scale
					label \"auto generated\"
					selected false
					"
			lappend NewNodes [stack 0]
			lappend ReadNodes [stack 0]
			}

		set rate [knob this.emission_rate]		
		# FRAME LOOP START
		 for {set cur_time 0} {[expression [knob this.start]+$cur_time] < [knob this.stop]} {set cur_time [expression $cur_time+1/$rate]} {
			foreach emitPoint $emissionPoints {
				puts "emission point at $emitPoint"
				push 0
				# ASSIGN TEXTURES #############################################################
				Switch {}
				set curNode [stack 0]
				knob $curNode.label "auto generated"
				in $curNode.which {
					set_expression "rint(random($counter,parent.sp_seed) * ([llength $ReadNodes]- 1))"
					}
				set in_pipe 0
				foreach cur_read $ReadNodes {input $curNode $in_pipe $cur_read; incr in_pipe}
				knob $curNode.selected false
				lappend NewNodes $curNode

				# TIME OFFSETS #############################################################
				TimeOffset {}
				set curNode [stack 0]
				knob $curNode.label "auto generated"
				set cur_upstream [value $curNode.input.which]
				set cur_img [value [topnode $curNode].name]
				set cur_last [value $cur_img.last_frame]
				in $curNode.time_offset {
					set_expression "(parent.start+$cur_time-1)+rint(parent.time_var * $cur_last * random($cur_time,parent.time_seed))"
					}
				knob $curNode.selected false
				lappend NewNodes $curNode

				# Multiply node, SCALE CURVES #############################################################
				Multiply {}
				set curNode [stack 0]
				in $curNode {
					addUserKnob 20 Curves
					addUserKnob 7 fade_in_curve l {fade in curve}
					addUserKnob 7 fade_out_curve l {fade out curve}
					addUserKnob 7 seed l seed
					addUserKnob 7 local_time l {local time}
					addUserKnob 7 grow_curve l {grow curve}
					addUserKnob 7 shrink_curve l {shrink curve}
					knob channels rgba
					knob value {{this.fade_in_curve*this.fade_out_curve}}
					knob label "auto generated"
					knob fade_in_curve "{\"clamp( ( (frame-parent.start-$cur_time+1) / (1+parent.fade_in_for) ) )\"}"
					knob fade_out_curve "{\"1-clamp( ( (frame-parent.start-$cur_time-parent.life_span+parent.fade_out_for+1) / (1+parent.fade_out_for) ) )\"}"
					knob seed "{\"random ($cur_time,parent.size_seed)\"}"
					knob local_time "{(frame-parent.start-$cur_time)/([value parent.life_span]-1)}"
					knob grow_curve "{\"clamp( ( (frame-parent.start-$cur_time+1) / (1+parent.grow_for) ) )\"}"
					knob shrink_curve "{\"1-clamp( ( (frame-parent.start-$cur_time-parent.life_span+parent.shrink_for+1) / (1+parent.shrink_for) ) )\"}"
					}
				lappend NewNodes $curNode



				# GEO AND VISIBILITY #############################################################
				ApplyMaterial {}
				set curGeo [stack 0]
				knob $curGeo.label "auto generated"
				input $curGeo 0 particleGeo
				input $curGeo 1 $curNode
				lappend NewNodes $curGeo


				# SPEED, ROTATION,SCALE #############################################################
				TransformGeo {}
				set curNode [stack 0]
				in $curNode {
					addUserKnob 20 User
					addUserKnob 7 seed l seed
					addUserKnob 7 rot_seed l rot_seed
					knob seed "{\"random ($cur_time,parent.speed_seed)\"}"
					knob rot_seed "{\"random ($cur_time,parent.rotation_seed)\"}"
					knob selectable false
					knob label "auto generated"
					in translate.z {
						set_expression "
							!input.disable *\
							(\
							-parent.normCurve(frame-parent.start-$cur_time) *\
							(1+(random ($cur_time,this.seed) * 2 - 1)*parent.speed_var) *\
							(parent.speed)\
							)"
						}
					in rotate.x {
							set_expression "\
								!input.disable *\
								parent.orientation.x -\
								parent.normCurve(frame-parent.start+$cur_time) *\
								(1+(random ($cur_time,this.rot_seed) * 2 - 1) * parent.rotation_var) *\
								parent.local_rot.x\
								"
						}
					in rotate.y {
						set_expression "\
							!input.disable * parent.orientation.y -\
							parent.normCurve(frame-parent.start+$cur_time) *\
							(1+(random ($cur_time,this.rot_seed) * 2 - 1)*parent.rotation_var) *\
							parent.local_rot.y\
							"
						}
					in rotate.z {
						set_expression "\
							!input.disable * parent.orientation.z -\
							parent.normCurve(frame-parent.start+$cur_time) *\
							(1+(random ($cur_time,this.rot_seed) * 2 - 1)*parent.rotation_var) *\
							parent.local_rot.z\
							"
						}
					in uniform_scale {
						set_expression "
							parent.size*input.input1.grow_curve * input.input1.shrink_curve +\
							((random(random($cur_time*1000000),input.input1.seed) * 2 - 1) * parent.size_var*parent.size)\
							"
							}
					# for input pipe/ApplyMaterial node:
			#			knob $curNode.uniform_scale "{\"parent.size*input.input1.grow_curve*input.input1.shrink_curve + ((random($cur_time,input.input1.seed)*2-1)*parent.size_var*parent.size)\"}"
					knob name "LocalMotion_$counter"
					}
				lappend NewNodes $curNode

				# SPREAD + PARENT MOTION #############################################################
				TransformGeo {}
				set curNode [stack 0]
				in $curNode {
					addUserKnob 20 User
					addUserKnob 7 seed l seed
					knob seed "{\"random ($cur_time,parent.spread_seed)\"}"
					knob rot_order "YXZ"
					knob label "auto generated"
					if {[class input1] == "Axis"} {
						in translate.x {
							set_expression "\
								((1-parent.inherit_velocity) *\
								parent.input1.translate.x(parent.normCurve($cur_time+parent.start)) +\
								parent.inherit_velocity*parent.input1.translate.x)\
								"
							}
						in translate.y {
							set_expression "\
								((1-parent.inherit_velocity) *\
								parent.input1.translate.y(parent.normCurve($cur_time+parent.start)) +\
								parent.inherit_velocity*parent.input1.translate.y)\
								"
							}
						in translate.z {
								set_expression "\
									((1-parent.inherit_velocity) *\
									parent.input1.translate.z(parent.normCurve($cur_time+parent.start)) +\
									parent.inherit_velocity*parent.input1.translate.z)\
								"
							}
						in rotate.x {
							set_expression "\
								((1-parent.inherit_velocity) *\
								(\[exists input1\]?parent.input1.rotate.x(parent.normCurve($cur_time+parent.start)) : 0) +\
								parent.inherit_velocity *\
								(\[exists input1\]?parent.input1.rotate.x:0)) +\
								parent.spread_yz * (2*random(this.seed, $cur_time*100,1)-1)\
								"
							}
						in rotate.y {
							set_expression "\
								((1-parent.inherit_velocity) *\
								(\[exists input1\]?parent.input1.rotate.y(parent.normCurve($cur_time+parent.start)) : 0) +\
								parent.inherit_velocity *\
								(\[exists input1\]?parent.input1.rotate.y:0)) +\
								parent.spread_xz * (2*random(this.seed+5, $cur_time*100,2)-1)\
								"
							}	
						in rotate.z {
							set_expression "\
								((1-parent.inherit_velocity) *\
								(\[exists input1\]?parent.input1.rotate.z(parent.normCurve($cur_time+parent.start)) : 0) +\
								parent.inherit_velocity *\
								(\[exists input1\]?parent.input1.rotate.z:0))\
								"
							}
					} else {
						knob translate $emitPoint
						in rotate.x {
							set_expression "\
								((1-parent.inherit_velocity) *\
								(\[exists input1\]?parent.input1.rotate.x(parent.normCurve($cur_time+parent.start)) : 0) +\
								parent.inherit_velocity *\
								(\[exists input1\]?parent.input1.rotate.x:0)) +\
								parent.spread_yz * (2*random(this.seed, $cur_time*100,1)-1)\
								"
							}
						in rotate.y {
							set_expression "\
								((1-parent.inherit_velocity) *\
								(\[exists input1\]?parent.input1.rotate.y(parent.normCurve($cur_time+parent.start)) : 0) +\
								parent.inherit_velocity *\
								(\[exists input1\]?parent.input1.rotate.y:0)) +\
								parent.spread_xz * (2*random(this.seed+5, $cur_time*100,2)-1)\
								"
							}	
						in rotate.z {
							set_expression "\
								((1-parent.inherit_velocity) *\
								(\[exists input1\]?parent.input1.rotate.z(parent.normCurve($cur_time+parent.start)) : 0) +\
								parent.inherit_velocity *\
								(\[exists input1\]?parent.input1.rotate.z:0))\
								"
							}												
						}
					knob name "Spread_$counter"
					#input $curNode 1 Emitter
					}
				lappend NewNodes $curNode

				# FORCES #############################################################
				TransformGeo {}
				set curNode [stack 0]
				in $curNode {
					knob selectable false
					knob rotate_z false
					in translate.x {
						set_expression "(pow(frame-parent.start-$cur_time,2) * parent.wind.x)"
						}
					in translate.y {
						set_expression "(pow(frame-parent.start-$cur_time,2) * -parent.gravity/100) + (pow(frame-parent.start-$cur_time,2) * parent.wind.y)"
						}
					in translate.z {
						set_expression "(pow(frame-parent.start-$cur_time,2) * parent.wind.z)"
						}
					input $curNode 2 lookAt
					knob name "Forces_$counter"
					knob label "auto generated"
					}
				knob $curNode.display {{"inrange (input.input.input.input1.local_time,0,1)?6:0"}}
				knob $curNode.render_mode {{"inrange (input.input.input.input1.local_time,0,1)?3:0"}}
				lappend NewNodes $curNode
				## SCENE NODES #############################################################
				## NEED TO DO THIS TO GET AROUND THE LIMIT OF 999 INPUTS PER SCENE NODE
				set inputLimit 999
				set scIndex [expression int(floor(($counter-1)/$inputLimit))]
				set curPipe [expression int(fmod(($counter-1),$inputLimit))]
#				puts "checking for Scene$scIndex"
				if ![exists this.Scene$scIndex] {
	#				puts "creating Scene Node $scIndex"
					Scene "name Scene$scIndex label \"auto generated\""
					set curScene [stack 0]
					input MasterScene $scIndex $curScene
					}
				puts "connecting particle $counter to pipe $curPipe of Scene$scIndex"
				input Scene$scIndex $curPipe $curNode

				## END OF NODE GENERATION #############################################################

				incr counter
				}
		}
		eval [concat autoplace $NewNodes]
		knob output "live"
	}
}


