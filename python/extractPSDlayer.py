import nuke

#	Created by Steve Morel - 28.03.2011
#	v1.0
#	www.stevemorel.com
#
#	Input : ReadNode with a PSD that contain layers named 'ps_'...
#	Output : Tree with the separate layer with crop, premult, card, linked to a scene, with camera / scanline render.
#
#	This script extract each layer named 'ps_'something of a 8bit PSD with a Shuffle Node.
#	Then it add a Premult Node, a Crop Node, and a Card.
#	The script also add a basic scene setup with a Scene Node, a Camera, and a ScanlineRender Node.
#	Each card are connected to this Scene Node.
#
#	layer name must begin with a 'ps_' to be catched.


def extractPSDlayer():
	#layer_begin: customisable variable to change the begining of the layer's name 'scanned' by the script.
	layer_begin = 'ps_'
	# read is the selected read node that load the PSD. You need to select it before running the script.
	read = nuke.selectedNode()
	# curPos record the read node position.
	curPos = (read['xpos'].value(), read['ypos'].value())
	# psd_chan records the channel of the psd.
	psd_chan = read.channels()
	# i is used to place the shuffle in the graph.
	i = 0

	# camera, scanlineRender, and scene creation.
	cam = nuke.nodes.Camera()
	cam.setXYpos( int(curPos[0] - 140), int(curPos[1]+380) )
	render = nuke.nodes.ScanlineRender()
	render.setXYpos( int(curPos[0]), int(curPos[1]+400) )
	scene = nuke.nodes.Scene()
	scene.setXYpos( int(curPos[0] + 10), int(curPos[1]+300) )
	render.setInput(1, scene)
	render.setInput(2, cam)

	# scanning psd chan.
	for chan in psd_chan:
		psd_chan_name = chan.split('.')[0]
		find_sub = psd_chan_name.find(layer_begin)
		if find_sub == 0 and psd_chan_name != psd_chan_name_test :
			# create shuffle, change its name, and the chan "in 1".
			my_shuffle = nuke.createNode('Shuffle', inpanel = False)
			my_shuffle['in'].setValue(psd_chan_name)
			my_shuffle['name'].setValue(psd_chan_name)
			my_shuffle.setXYpos( int(curPos[0]+i*100 ), int(curPos[1]+100) )
			i += 1
			# add the premult node, and the crop node.
			my_premult = nuke.createNode('Premult', inpanel = False)
			my_premult['postage_stamp'].setValue(True)
			my_crop = nuke.createNode('Crop', inpanel = False)
			# add the card, and connect it to the scene.
			my_card = nuke.createNode('Card', inpanel = False)
			my_shuffle.setInput(0, read)
			scene.setInput(i, my_card)

		# psd_chan_name_test record the psd_chan_name to avoid creating multiple shuffle for R / G / B / A chan.
		psd_chan_name_test = psd_chan_name