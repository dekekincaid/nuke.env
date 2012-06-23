#written by frank rueter
#last update	May 24, 2006
#		July 17, 2007	- fixed expression assignment for single fields in array knobs
#				- fixed bug where "open control panel" wouldn't work

###################
# opens a panel to view and modify all expressions in the script or the current selection
# if an expression produces an error the respective label turns red
#
# known bug: if knobs are referenced without a preceding node name (i.e. "size*5" or "this.size*5" instead of "Blur1.size*5") the panel will show an error as the result
# because the expression is not parsed in the node's context. However, the label should not turn red indicating that it's a valid expression in the node itself.
#
###################
proc ExpressionManager {SourceNodes} {
puts "\nAnalyzing expressions...\n"
	array set expressionKnobs {}
	foreach cur_node $SourceNodes {
		foreach cur_knob [knobs -d $cur_node] {
			#need to do this cause "has_expression" doesn't work for some knobs auch as "format"
			if ![catch {value $cur_node.$cur_knob.has_expression}] {
				#collect knobs with expressions
				if [value $cur_node.$cur_knob.has_expression] {
					set fields [llength [knob $cur_node.$cur_knob]]
					for {set cur_field 0} {$cur_field < $fields} {incr cur_field} { 
						if ![value $cur_node.$cur_knob.$cur_field.has_expression] {
							puts "[value $cur_node.name].$cur_knob.$cur_field has no expression"
							continue
							}
						
						set curExpression [knob $cur_node.$cur_knob.$cur_field]
						#puts "collecting expressions...[value $cur_node.name].$cur_knob.$cur_field:\n$curExpression"
						set cleanExpression [lindex [lindex $curExpression 0] 0]
						set expressionKnob [value $cur_node.name].$cur_knob.$cur_field
						set expressionKnobs($expressionKnob) $cleanExpression

						#debug on
						#message "input:\n$curExpression\nclean up:\n$cleanExpression"
						#debug off
							
						}
					}
				}
			}
		}
	if {[llength [array names expressionKnobs]] > 0} {
		set panelText ""
		array set outputX {}
		#build ui
		foreach cur_knob [lsort -dictionary [array names expressionKnobs]] {
			set CurNode [lindex [split $cur_knob "."] 0]
			set X_$cur_knob $expressionKnobs($cur_knob)
			#set label colour to red if expression returns an error current' node's context
			if [catch {in $CurNode {expression $expressionKnobs($cur_knob)}} errorMsg] {set colour "@B1;"} else {set colour "@B49;"}
			append panelText "{\"$colour$cur_knob \" X_$cur_knob x} \
			{\"@recycle;update expression\" update_$cur_knob b} \
			{\"@icon_tab;open control panel\" openPanel_$cur_knob b} \
			"
			}
		if [catch {
			panel -w800 "Expression Manager" $panelText
			}] {return}
		#hit 'ok' to update expressions for selected knobs
		foreach cur_knob [lsort -dictionary [array names expressionKnobs]] {
			set CurNode [lindex [split $cur_knob "."] 0]
			if [append update_$cur_knob] {
				set X_Out [append X_$cur_knob]
				#debug on
				#puts "$cur_knob\ncompressed: $cur_knob\noutput:\n$cur_knob -> $X_Out\n"
				#debug off
				
				in $cur_knob {set_expression $X_Out}
				}
			if [append openPanel_$cur_knob] {show $CurNode}
			}
		} else {message "no expressions found."}
	}
