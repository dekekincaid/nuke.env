# Duplicate Read Destroyer
# By Nathan Rusch
# Updated June 17, 2010

import nuke

def dupReadDestroy(useSelection=False):
	'''
	Eliminates Read nodes with duplicate paths. 
	Replaces all but the upper-most sibling in the DAG with PostageStamp nodes.
	Returns a list of the remaining read nodes from the input set.
	Optional boolean argument specifies whether or not to limit operation to the current node selection.
	'''
	if useSelection:
		readNodes = nuke.selectedNodes("Read")
	else:
		readNodes = nuke.allNodes("Read")
	if not readNodes:
		return

	readPaths = [node['file'].value() for node in readNodes]
	dupNodes = []

	for node in readNodes:
		dupSet = []
		if readPaths.count(node['file'].value()) > 1:
			dupSet = [i for i in readNodes if i['file'].value() == node['file'].value()]
			dupNodes.append(dupSet)
			for dup in dupSet:
				readNodes.remove(dup)
				readPaths.remove(dup['file'].value())

	if dupNodes:
		for set in dupNodes:
			yPos = [node.ypos() for node in set]
			yPos.sort()
			keep = [n for n in set if n.ypos() == yPos[0]][0]
			set.remove(keep)
			for node in set:
				node.setSelected(True)
				ps = nuke.createNode("PostageStamp", "name PStamp_%s label %s hide_input True postage_stamp True xpos %d ypos %d tile_color 3281491967" % (node.name(), node.name(), node.xpos(), node.ypos()), False)
				ps.setInput(0, keep)
				ps.setSelected(False)
				nuke.delete(node)

	if useSelection:
		return nuke.selectedNodes("Read")
	else:
		return nuke.allNodes("Read")