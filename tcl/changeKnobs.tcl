proc changeKnobs {} {
		set curClass [class [stack 0]]
		foreach cur_node [selected_nodes] {
			if {$curClass != [class $cur_node]} {
				return "more than one node type selected"
				} else {
				set curClass [class $cur_node]
				}
			}
		
		if ![catch {panel -w500 "change multiple knobs" {
		{"knob name" targetKnob}
		{"new value" newValue x}
		{"result" pulldown e {absolute add multiply}}
		}}] {
		foreach cur_node [selected_nodes] {
			switch $pulldown {
				absolute {
					knob $cur_node.$targetKnob $newValue
					}
				add {
					knob $cur_node.$targetKnob [expr [knob $cur_node.$targetKnob] + $newValue]
					}
				multiply {
					knob $cur_node.$targetKnob [expr [knob $cur_node.$targetKnob] * $newValue]
					}
				}
			}
		}

}
