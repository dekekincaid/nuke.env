
import os
import subprocess

def revealInOS():
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b) [0]
    u = os.path.normpath (u)
    print u
#osx
    subprocess.Popen(['open', '-R', '%s' % (u)])
#gnome
	subprocess.Popen(['nautilus','%s' % (u)])
#kde
	subprocess.Popen(['nautilus','%s' % (u)])

#windows
    cmd = 'explorer "%s"' % (u)
    print cmd
    os.system(cmd)	

