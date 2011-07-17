###    add bookmarks to the DAG which are 
###    retrievable and DAG zooms to them
###
###    written by Howard Jones  and  Diogo Girondi 2009
###    bookmarkthis() and cyclebookmarks() written by Diogo Girondi modified by Howard Jones
###    listbookmarks() written by Howard Jones
###    v1.1.4- Last modified: 30/01/10



import nuke
import string
import re
bookmarks = None

def bookmarkthis( desc=True, ask=True ):
    
    '''Bookmarks a node for quick navigation'''

    try:
        sn = nuke.selectedNodes()[-1]
    except:
        nuke.message('Please select a node')
        sn = None
    
    if sn is not None:

        if sn['icon'].value() != 'bookmark.png' and desc == True:
            l=sn['label'].value()
            panel = nuke.Panel ('Bookmark This',300)     
            panel.addSingleLineInput('add description',l)
            result=panel.show()
            d = panel.value('add description')

            if result:
                sn['icon'].setValue('bookmark.png')
                sn['label'].setValue(d)
        else:
            if ask:
                clear=nuke.ask('Clear Bookmark and Label?')
                if clear:
                    sn['icon'].setValue('')
                    sn['label'].setValue('')
            else:
                if desc:
                    sn['icon'].setValue('')
                    sn['label'].setValue('')
                else:
                    sn['icon'].setValue('')
                

def listbookmarks():
    
    bm=[]
    zoomBy=1

    #find bookmark nodes
    for n in nuke.allNodes():
        n['selected'].setValue( False )
        if n['icon'].value() == 'bookmark.png':
            n['selected'].setValue( True )      #select nodes for clarity
            bmLabel=nuke.selectedNode()['label'].value() 

            if bmLabel:
                bm_name='"'+bmLabel+'"' # '"'<-lets it list correctly
            else:
                bm_name='"'+n.name()+'"' # '"'<-allows it to be sorted correctly with above
            bm.append(bm_name)
    if 0==len(bm):
        nuke.message('no bookmarks found')
    else:
        bookmarkList=str(sorted(bm))  

        #clean up list name
        pattern = re.compile('[\[\]\']')
        bookmarkList = pattern.sub('', bookmarkList)
        pattern = re.compile('[\,]')
        bookmarkList = pattern.sub(' ', bookmarkList)

           
        #let user choose bookmark
        panel = nuke.Panel ('BookMarks',200)     
        panel.addEnumerationPulldown('go to',bookmarkList)
        panel.addSingleLineInput('zoom',zoomBy)
        panel.addBooleanCheckBox('also open node', False)          
        panel.addButton("Cancel")
        panel.addButton("Zoom to")
        panel.addButton("Open")
        result=panel.show()

        if result:
            goto= panel.value('go to')
            zoomf= panel.value('zoom')
            alwaysOpen= panel.value('also open node')

            #select only relevent node
            for n in nuke.allNodes():
                if goto == n.name() or goto == n['label'].value():
                    n['selected'].setValue( True )
                else:
                    n['selected'].setValue( False )

            #set nuke to highlight chosen node, get xy pos and zoom into area and open if selected.
            if result ==1:                  
                nuke.zoom(float(zoomf),(nuke.selectedNode().xpos(),nuke.selectedNode().ypos()))
                if alwaysOpen:
                    nuke.show(nuke.selectedNode())
            elif result ==2:                  
                nuke.show(nuke.selectedNode())
            else:
                pass
            

def cyclebookmarks( prt=False ):
    
    '''Cycles between existent bookmarks'''
    
    global bookmarks
    if prt:
        print bookmarks
    
    if bookmarks is None:
        bookmarks = iter([n for n in nuke.allNodes() if n['icon'].value() == 'bookmark.png'])
        if prt:
            print bookmarks
    
    try:
        n = bookmarks.next()
        n['selected'].setValue( True )
        if prt:
            print n['label'].value()

    except:
        bookmarks = iter([n for n in nuke.allNodes() if n['icon'].value() == 'bookmark.png'])
    
    goTo = nuke.zoom(1,(n.xpos(),n.ypos()))


