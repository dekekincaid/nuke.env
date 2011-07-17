#written by frank rueter
#last update	May 23, 2006
###################
# parses all expressions in a script (or in the current node selection) and opens a panel with info about any expressions that produce errors
###################
proc CheckExpressions {SourceNodes} {
	set ErrorText "expression errors in current script:\n\n"
	set errorNodes {}
	set errorID 0
	foreach cur_node $SourceNodes {
		foreach cur_knob [knobs -d $cur_node] {
			#need to do this cause "has_expression" doesn't work for some knobs auch as "format"
			if ![catch {value $cur_node.$cur_knob.has_expression}] {
				#collect knobs with expressions
				if [value $cur_node.$cur_knob.has_expression] {
					set NodeName [value $cur_node.name]
					puts "testing [knob $cur_node.$cur_knob] in $NodeName"
					if [catch {expression $cur_node.$cur_knob} errorMsg] {
						set badExpression [string trim [knob $cur_node.$cur_knob] "{}i"]
						append errorText "error in [value $cur_node.name].$cur_knob:\n$badExpression >>  $errorMsg\n\n"
						lappend errorNodes $cur_node
						incr errorID
						}
					}
				}
			}
		}
	#if $errorID {alert $errorText}
	if {$errorID > 0} {
		if [catch {
			panel -w800 "expression errors" "
				{\"bad expressions \" errorText n[expr $errorID*3]}
				{\"open control panel\" openPanel b}
			"
			}] {return}
		if $openPanel {foreach curNode $errorNodes {show $curNode}}
		} else {message "all is good"}
	}

