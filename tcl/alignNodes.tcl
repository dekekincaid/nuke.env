######  
# by frankr@wetafx.co.nz
# aligns selectyed nodes in the DAG over X or Y depending on the provided argument ("xpos" or "ypos")
# last modified:
#	25.11.2005
#	09.01.2006 - added description
######  
proc alignNodes {orientation} {

set allPos 0
set nodeCount 0

foreach cur_node [selected_nodes] {
	incr nodeCount
	set curPos [knob $cur_node.$orientation]
	set allPos [expr $allPos+$curPos]
	}
set averagePos [expr $allPos/$nodeCount]
foreach cur_node [selected_nodes] {
	knob $cur_node.$orientation $averagePos
	}

}

