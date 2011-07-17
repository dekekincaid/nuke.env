#written by frankr
#last update 11.01.2006 - added description
###################
# pastes the clipboard for each selected node and connects it downstream
###################

proc PasteToSelected {} {
	set selection [selected_nodes]
	foreach cur_node $selection {
		knob $cur_node.selected 0	
		}
			
	foreach cur_node $selection {
		knob $cur_node.selected 1
		node_paste [cut_paste_file]
		foreach cur_sel [selected_nodes] {
			knob $cur_sel.selected 0	
			}
		}

	foreach cur_node $selection {
		knob $cur_node.selected 1
		}
	
	}

