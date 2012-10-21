#
# autowrite.py
#
# Tim BOWMAN [puffy@netherlogic.com]
#
# Semi-automatic Write node output paths lead to fewer user errors and greater
# consistency in file-naming.
#

import nuke

def dropAutoWrite():
    """
    Creates an automatic Write node (an "AutoWrite") which uses the name and 
    path of the Nuke script that it's in to create it's own output path.
    
    Changes made to the script's name (such as versioning up) wil be reflected 
    in the output path auto-magically with no user intervention.
    """
    
    # Create the Write node that will become an AutoWrite
    w= nuke.createNode('Write', inpanel=False)
    # Rename it to AutoWrite
    # (Also, deal with the number problem)
    count = 1
    while nuke.exists('AutoWrite' + str(count)):
        count += 1
    w.knob('name').setValue('AutoWrite' + str(count))
    
    # Add the tab to hold the variables containing path fragments so we can have
    # a less messy file path.
    t = nuke.Tab_Knob("Path Fragments")
    w.addKnob(t)
    w.addKnob(nuke.EvalString_Knob('proj_root', 'Project Root', '[join [lrange [split [value root.name] / ] 0 4 ] / ]'))
    w.addKnob(nuke.EvalString_Knob('seq', 'Sequence', '[lrange [split [value root.name] / ] 5 5 ]'))
    w.addKnob(nuke.EvalString_Knob('shot', 'Shot Name', '[lrange [split [value root.name] / ] 6 6 ]'))
    w.addKnob(nuke.EvalString_Knob('script', 'Script Name', '[file rootname [file tail [value root.name] ] ]'))
    
    # Display the values of our path fragment knobs on the node in the DAG for
    # error-checking.
    # This can be turned off if it makes too much of a mess for your taste.
    feedback = """
    Output Path: [value file]
    
    Project Root: [value proj_root]
    Sequence: [value seq]
    Shot Name: [value shot]
    Script Name: [value script]
    """
    w.knob('label').setValue(feedback)
    
    # Re-assemble the path fragments into a proper output path
    output_path = "[value proj_root]/[value seq]/[value shot]/comps/[value script]/[value input.width]x[value input.height]/[value script].%04d.dpx"
    w.knob('file').fromScript(output_path)


# Add an AutoWrite option to the Image menu
nuke.tprint('Adding AutoWrite to Image menu.')
menubar=nuke.menu('Nodes')
m = menubar.findItem('Image')
m.addSeparator()
m.addCommand('AutoWrite', 'autowrite.dropAutoWrite()')
