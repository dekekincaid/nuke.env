import os, nuke

def getFileInfos():
    fullPath = nuke.Root().knob('name').getValue()
    dir = os.path.dirname(fullPath)
    dir += "/"
    basename = os.path.basename(fullPath)
    name = os.path.splitext(basename)[0]
    show = ""
    scene = ""
    shot = ""
    version = ""
    valid = True
    format = ""

    try:
        show,scene,shot,version = name.split('_')
        format = "long"
    except:
        try:
            show,shot,version = name.split('_')
            format = "middle"
        except:
            try:
                shot,version = name.split('_')
                format = "short"
            except:
                nuke.message("Bad Filename Format! \n\nFilename should either look like 'Show_Scene_Shot_Version', 'Show_Shot_Version' or 'Shot_Version'.")
                valid = False

    return dir,name,show,scene,shot,version,valid,format


def autoFillWrite():
    
    dir,name,show,scene,shot,version,valid,format = getFileInfos()

    # standard values for creation
    numberformat = "%04d"
    extension = "sgi"

    if valid:
        selection = nuke.selectedNodes('Write')
        
        for node in selection:
            try:

                try:
                    # try to set standard values
                    node['show'].setValue(show)
                    node['applyShow'].setValue("Filename")
                    node['scene'].setValue(scene)
                    node['applyScene'].setValue("Filename")
                    node['shot'].setValue(shot)
                    node['applyShot'].setValue("Filename")
                    node['custom'].setValue("")
                    node['applyCustom'].setValue("None")
                    node['path'].setValue(dir)
                    node['number'].setValue(numberformat)
                    node['file_type'].setValue(extension)

                # node is no autoFillWrite yet, so create user knobs
                except:

                    # show 
                    user_show = nuke.String_Knob("show", "show: ", show)
                    node.addKnob(user_show)
                    node['show'].setFlag(nuke.STARTLINE)
                    if not format == "short":
                        user_applyShow = nuke.Enumeration_Knob('applyShow', '', ['None','Folder', 'Filename', 'Both'])
                        node.addKnob(user_applyShow)
                        node['applyShow'].clearFlag(nuke.STARTLINE)
                        node['applyShow'].setValue("Filename")
                    else:
                        node['show'].setFlag(nuke.INVISIBLE)        

                    # scene
                    user_scene = nuke.String_Knob("scene", "scene: ", scene)
                    node.addKnob(user_scene)
                    node['scene'].setFlag(nuke.STARTLINE)
                    if format == "long":
                        user_applyScene = nuke.Enumeration_Knob('applyScene', '', ['None','Folder', 'Filename', 'Both'])
                        node.addKnob(user_applyScene)
                        node['applyScene'].clearFlag(nuke.STARTLINE)
                        node['applyScene'].setValue("Filename")
                    else:
                        node['scene'].setFlag(nuke.INVISIBLE)

                    # shot
                    user_shot = nuke.String_Knob("shot", "shot: ", shot)
                    node.addKnob(user_shot)
                    node['shot'].setFlag(nuke.STARTLINE)
    
                    user_applyShot = nuke.Enumeration_Knob('applyShot', '', ['None','Folder', 'Filename', 'Both'])
                    node.addKnob(user_applyShot)
                    node['applyShot'].clearFlag(nuke.STARTLINE)
                    node['applyShot'].setValue("Filename")

                    # custom
                    user_custom = nuke.String_Knob("custom", "custom postfix: ", "")
                    node.addKnob(user_custom)
                    node['custom'].setFlag(nuke.STARTLINE)
    
                    user_applyCustom = nuke.Enumeration_Knob('applyCustom', '', ['None','Folder', 'Filename', 'Both'])
                    node.addKnob(user_applyCustom)
                    node['applyCustom'].clearFlag(nuke.STARTLINE)
                    node['applyCustom'].setValue("None")

                    # path
                    user_path = nuke.File_Knob("path", "path: ")
                    node.addKnob(user_path)
                    node['path'].setValue(dir)
                    node['path'].setFlag(nuke.STARTLINE)
    
                    # number format
                    user_number = nuke.Enumeration_Knob('number', 'numberformat: ', ['%01d','%02d', '%03d', '%04d', '%05d', 'custom'])
                    node.addKnob(user_number)
                    node['number'].setFlag(nuke.STARTLINE)
                    node['number'].setValue("%04d")

                    user_number_custom = nuke.String_Knob("number_custom", "", "custom format")
                    node.addKnob(user_number_custom)
                    node['number_custom'].clearFlag(nuke.STARTLINE)
                    node['number_custom'].setEnabled(False)
    
                    # file type
                    node.addKnob(node['file_type'])
                    node['file_type'].setValue(extension)

                    # set write settings
                    node.knob('file').setValue(dir + version + "/" + name + "_" + numberformat + "." + extension)
                    node.knob('proxy').setValue(dir +  version + "/" + name + "_proxy_" + numberformat + "." + extension)
                    node.knob('datatype').setValue("16 Bit")
                    node.knob('label').setValue("autoFillWrite")

            except:
                # something went terribly wrong and we all gonna die ...
                nuke.message("Couldn't change Settings for Write Node")



def updateAutoFillWrite():

    dir,name,show,scene,shot,version,valid,format = getFileInfos()
    
    if valid:
        selection = nuke.allNodes('Write')
     
        # find autoFillWrite nodes
        for node in selection:
            if node.knob('label').value() == "autoFillWrite":
                try:
                    # Get Settings

                    # show
                    if not format == "short":
                        applyShow = node['applyShow'].value()
                        if applyShow == "Folder":
                            show_folder = node['show'].value() + "_"
                            show_filename = ""
                            
                        elif applyShow == "Filename":
                            show_folder = ""
                            show_filename = node['show'].value() + "_"
                        elif applyShow == "Both":
                            show_folder = node['show'].value() + "_"
                            show_filename = node['show'].value() + "_"
                        else:
                            show_folder = ""
                            show_filename = ""
                    else:
                        show_folder = ""
                        show_filename = ""

                    # scene
                    if format == "long":
                        applyScene = node['applyScene'].value()
                        if applyScene == "Folder":
                            scene_folder = node['scene'].value() + "_"
                            scene_filename = ""
                        elif applyScene == "Filename":
                            scene_folder = ""
                            scene_filename = node['scene'].value() + "_"
                        elif applyScene == "Both":
                            scene_folder = node['scene'].value() + "_"
                            scene_filename = node['scene'].value() + "_"
                        else:
                            scene_folder = ""
                            scene_filename = ""
                    else:
                        scene_folder = ""
                        scene_filename = ""

                    # shot
                    applyShot = node['applyShot'].value()
                    if applyShot == "Folder":
                        shot_folder = node['shot'].value() + "_"
                        shot_filename = ""
                    elif applyShot == "Filename":
                        shot_folder = ""
                        shot_filename = node['shot'].value() + "_"
                    elif applyShot == "Both":
                        shot_folder = node['shot'].value() + "_"
                        shot_filename = node['shot'].value() + "_"
                    else:
                        shot_folder = ""
                        shot_filename = ""

                    # custom
                    applyCustom = node['applyCustom'].value()
                    if applyCustom == "Folder":
                        custom_folder = node['custom'].value() + "_"
                        custom_filename = ""
                    elif applyCustom == "Filename":
                        custom_folder = ""
                        custom_filename = node['custom'].value() + "_"
                    elif applyCustom == "Both":
                        custom_folder = node['custom'].value() + "_"
                        custom_filename = node['custom'].value() + "_"
                    else:
                        custom_folder = ""
                        custom_filename = ""

                    # number
                    number = node['number'].value()
                    if number == "custom":
                        node['number_custom'].setEnabled(True)
                        number = "_" + node['number_custom'].value()
                    else:
                        node['number_custom'].setEnabled(False)
                        number = "_" + number;
    
                    # rest
                    path = node['path'].value()
                    extension = node['file_type'].value()
                    if extension == "mov":
                        number = ""

                    # Update Write Node
                    node['file'].setValue(path + show_folder + scene_folder + shot_folder + custom_folder + version + "/" + show_filename + scene_filename + shot_filename + custom_filename +  version +  number + "." + extension)
                    node['proxy'].setValue(path + show_folder + scene_folder + shot_folder + custom_folder + version + "/" + show_filename + scene_filename + shot_filename + custom_filename +  version +  "_proxy" +  number + "." + extension)

                    if extension == "sgi":
                        node['datatype'].setValue("16 Bit")
                except:
                    print("No AutoFillWrites found.")



def createOutputDir(): 
    file = nuke.filename(nuke.thisNode()) 
    dir = os.path.dirname( file ) 
    osdir = nuke.callbacks.filenameFilter( dir ) 
    if not os.path.isdir(osdir):
        os.makedirs(osdir)


# register functions
nuke.addOnScriptSave(updateAutoFillWrite)
nuke.addUpdateUI(updateAutoFillWrite, nodeClass='Write')
nuke.addBeforeRender(createOutputDir)

