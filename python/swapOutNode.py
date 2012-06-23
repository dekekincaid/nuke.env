'''
swapOutNode
By Nathan Rusch
Updated February 2, 2012

Changelog:
	v0.1.0: Started this changelog. First usable version.
	v0.1.1: Added ``getConnectedNodes`` function.
			Code cleanup/refactoring.
'''
import nuke
import nukescripts


def getConnectedNodes(node):
	'''
	Returns a two-tuple of lists. Each list is made up of two-tuples in the
	form ``(index, nodeObj)`` where 'index' is an input index and 'nodeObj'
	is a Nuke node.

	The first list contains the inputs to 'node', where each 'index' is the
	input index of 'node' itself.

	The second contains its outputs, where each 'index' is the input index that
	is connected to 'node'.
	'''
	inputNodes = [(i, node.input(i)) for i in range(node.inputs())]
	outputNodes = []
	for depNode in nuke.dependentNodes(nuke.INPUTS | nuke.HIDDEN_INPUTS, node):
		for i in range(depNode.inputs()):
			if depNode.input(i) == node:
				outputNodes.append((i, depNode))
	return (inputNodes, outputNodes)

def swapOutNode(targetNode, newNode):
	'''
	Mostly mimics the Ctrl + Shift + drag-and-drop node functionality in Nuke.

	'targetNode': The node (or node name) to be replaced.
	'newNode': The node (or node name) that will replace it.
	'''
	if isinstance(targetNode, basestring):
		targetNode = nuke.toNode(targetNode)
	if isinstance(newNode, basestring):
		newNode = nuke.toNode(newNode)
	if not (isinstance(targetNode, nuke.Node) and isinstance(newNode, nuke.Node)):
		return
	sourcePos = (newNode.xpos(), newNode.ypos())
	targetPos = (targetNode.xpos(), targetNode.ypos())
	oldSel = nuke.selectedNodes()
	inputNodes, outputNodes = getConnectedNodes(targetNode)
	nukescripts.clear_selection_recursive()
	targetNode.setSelected(True)
	nuke.extractSelected()
	targetNode.setSelected(False)
	newNode.setXYpos(*targetPos)
	targetNode.setXYpos(*sourcePos)
	for inNode in inputNodes:
		newNode.setInput(*inNode)
	for index, node in outputNodes:
		node.setInput(index, newNode)
	for node in oldSel:
		node.setSelected(True)
	return True
