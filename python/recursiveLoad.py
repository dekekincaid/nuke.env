# written by Howard Jones
# last modified 16th July 2011
# v1.0

import os, re, nuke, inspect

def lineno():
        return inspect.currentframe().f_back.f_lineno  


nameList=[]
filesFound=[]
ReadList=[]
verbose=False
inStereo=True
stereoReplace=[('/right/','/left/'),('_right_','_left_'),('_right-','_left-')] # (source,replace) for all right to left conversions needed to match paths and filenames

def splitImgSeqs(path, files):
  if verbose: print path
  #Get a list of unique names in file
  for i in files:
      sp=i.split('.')
      name=sp[0]
      ext=sp[-1]
      name2CheckFor=str(name)+'.'+str(ext)
      if name2CheckFor not in nameList:
          nameList.append(name2CheckFor)
  for n in nameList:
      curList=[]
      for i in files:
          if not str(path).endswith('/'):
            path+='/'
          if verbose: print path
  
          if n.split('.')[0] in i:
              if n.split('.')[-1] in i:
                  curList.append(path+i)
      if curList:
          filesFound.append(curList)
      filesFound.sort()
  return filesFound

def imgSeq2NukeFormat(filesFound):
    for ff in filesFound:
      if verbose: print 'ff :', ff
      #SHOULDN'T NEED TO LOOP AS SHOULD BE A SORTED LIST BUT THIS IS FAILING FOR SOME REASON SO WORKING THROUGH LIST TO GET START AND END
      #UNCOMMENT THE NEXT 2 LINES AND COMMENT TO ###END MINMAX###
      #start=ff[0].split('.')[-2]
      #end=ff[-1].split('.')[-2]
      minMax=[]
      for i in ff:
          frames=i.split('.')[-2]
          minMax.append(frames)
      start=min(minMax)
      end=max(minMax)
      ###END MINMAX###
      if verbose: print 'start ', start, 'end ', end

      #move on and ignore if the file is a hidden file
      if  ff[0].split('/')[-1].startswith('.'):
        print 'hidden file skipped'
        continue     
      path=ff[0].split('/')[0]
      splitFiles= ff[0].split('.')
      name=splitFiles[0]


      padNum=splitFiles[-2]
      if padNum.isdigit():
          padding =len(splitFiles[-2])*'#'
      else:
          padding=''
      ext=splitFiles[-1]
      
      if padding:
          readFile=path+name+'.'+padding+'.'+ext+' '+start+'-'+end
      else:
          readFile=path+name+'.'+ext
      ReadList.append(readFile)
    return ReadList   

def stereoMatch(fileName):
  #replace right strings with left strings to match paths and files
  for i in range(len(stereoReplace)):
    pattern = re.compile(stereoReplace[i][0])
    fileName = pattern.sub(stereoReplace[i][1], fileName)

  return fileName

def createReads(ReadList):
  #createdNodes=[]
  for r in ReadList:
      if r.split(' ')[0][-3:] not in ('obj', 'fbx'):
          if inStereo:
             if '/re/' in r:
                r_left=stereoMatch(r)
                rnleft=nuke.createNode('Read')
                rnright=nuke.createNode('Read')
                jv=nuke.createNode('JoinViews')
                rnleft['file'].fromUserText(r_left)
                rnright['file'].fromUserText(r)
                jv.setInput(0,rnleft)
                jv.setInput(1,rnright)
             elif '/le/' not in r:
                rn=nuke.createNode('Read')
                rn['file'].fromUserText(r)
          else:
             rn=nuke.createNode('Read')
             rn['file'].fromUserText(r)
      else:
          rn=nuke.createNode('ReadGeo')
          rn.setInput(0,None)
          rn['file'].fromUserText(r)
      #rn.setSelected(False)
      #createdNodes.append(rn)
  #for i in createdNodes: print i['file'].getValue()
      
def getPath4Walk(walkPath=''):
      directory=nuke.getClipname('Choose Folder',multiple=False)
      if verbose: print >> sys.stderr, 'failed here %s\n' % lineno()  
      return directory

def recursiveLoad(verbose=False):
    walkPath=getPath4Walk()
    if verbose: print walkPath
    
    #for roots, dirs, files in sorted(os.walk(dir2walk)):
    f=os.walk(walkPath)
    for i in f:
         filesFound=splitImgSeqs(i[0], i[-1])
    if verbose: print 'files found ', filesFound
    if verbose: print >> sys.stderr, 'failed here %s\n' % lineno()  
    
    readsList=imgSeq2NukeFormat(filesFound)
    
    if verbose: print (readsList)
    
    createReads(readsList)


 
 
