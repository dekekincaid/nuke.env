import os
import re

import nuke

def nfxMenu(menu='NFX', panel='Nodes'):
	'''
	Adds NFXPlugins to the menu in panel.
	'''

	pluginList = []

	plugins = nuke.plugins(nuke.ALL | nuke.NODIR, 'N_*.py', 'N_*.so', 'N_*.dylib', 'N_*.dll')

	for i in plugins:
		(root, ext) = os.path.splitext(i)

		if root is None or len(root) == 0:
			continue

		pluginList.append(root)

	if pluginList:
		pluginList.sort()

		m = nuke.menu(panel)

		if not m:
			raise RuntimeError, 'nfxMenu() argument 2 not found'

		for n in pluginList:
			m.addCommand(menu + '/' + n[2:], 'nuke.createNode("%s")' % n)

nfxMenu()
