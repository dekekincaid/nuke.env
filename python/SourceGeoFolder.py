##auteur:Lucien FOSTIER
##date:10/05/10

##Ce script va automatiser limport de geometrie 3D dans le node graph de nuke, il permet de selectionner un dossier par lintermediaire dun
##panneau pop up et de choisir entre deux extensions a importer soit toutes les geometries contenues dans le dossier en .obj soit en .fbx
##un read geo par file trouvee dans le dossier sera creer et la lecteur des coordonnees w pour les textures sera desactivee
##enfin un noeud scene sera creer pour relier les differents read geo

##developpe sur nuke5.2v3


import fnmatch,nuke,os

def SourceGeoFolder():

    extList="OBJ FBX"
    p=nuke.Panel("Source Geo folder")
    p.addFilenameSearch("Geo Folder:","")
    p.addEnumerationPulldown("extenstion:", extList)
    if p.show():

        path=p.value("Geo Folder:")
        extIndex=p.value("extenstion:")

        if extIndex=="OBJ":

            ext=".obj"

        else:

            ext=".fbx"

        fileList=[]

        for file in os.listdir(path):
            if fnmatch.fnmatch(file, '*'+ext):
                fileList.append(file)

        filepathList=[]

        for n in range(len(fileList)):
    
            filepathList.append(path+fileList[n])

        readGeoList=[]

        for i in range(len(filepathList)):

            currentfile=filepathList[i]
            node=nuke.nodes.ReadGeo(file=currentfile)
            node['read_texture_w_coord'].setValue(0)
            readGeoList.append(node)
    

        scene=nuke.nodes.Scene()


        for n in range( len(readGeoList)):


            currentReadNode=readGeoList[n]
            scene.setInput(n,currentReadNode)


