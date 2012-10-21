import os
import math
import nukescripts
import nuke

class DiskCachePanel(nukescripts.PythonPanel):
  def __init__(self):
    nukescripts.PythonPanel.__init__( self, 'DiskCache', 'uk.co.thefoundry.DiskCache')
    
    # CREATE KNOBS
    self.diskCachePrefText = nuke.Text_Knob('disk_cache_pref_GB','Disk cache limit:')
    self.addKnob( self.diskCachePrefText)
    self.diskCachePrefText.setValue('?GB')
    self.diskCachePercUsed = nuke.Double_Knob('disk_cache_pref_GB','% used:')
    self.addKnob( self.diskCachePercUsed)
    self.diskCachePercUsed.setValue(50)
    self.diskCachePercUsed.setRange(0,100)
    self.diskCachePercUsed.setEnabled(False)
   
    totalCacheGB = nuke.toNode('preferences').knob('diskCacheGB').value()
    
    self.diskCachePrefText.setValue(str(totalCacheGB) + 'GB')
 
    # Check if Major Version is 6 or later... 
    if nuke.env['NukeVersionMajor'] >= 6:
      self.paintCachePrefText = nuke.Text_Knob('paint_cache_pref_GB','Paint cache limit:')
      self.addKnob( self.paintCachePrefText)
      self.paintCachePrefText.setValue('?GB')
      self.paintCachePercUsed = nuke.Double_Knob('paint_cache_pref_GB','% used:')
      self.addKnob( self.paintCachePercUsed)
      self.paintCachePercUsed.setValue(50)
      self.paintCachePercUsed.setRange(0,100)
      self.paintCachePercUsed.setEnabled(False)
      self.paintCachePercUsed.setFlag(0x00002000)
	  
      paintCacheGB = nuke.toNode('preferences').knob('PaintCacheGB').value()
      self.paintCachePrefText.setValue(str(paintCacheGB) + 'GB')
      
    # Update Cache usage button
    self.updateButton = nuke.Script_Knob('update','Update')
    self.addKnob(self.updateButton) 
    
    # Clear DiskCacheButton   
    self.clearCacheButton = nuke.Script_Knob('clearCache','Clear Disk Cache')
    self.addKnob(self.clearCacheButton) 
    
    self.addKnob(nuke.Text_Knob('',''))
	
    # Clear Buffer Button
    self.clearBuffers = nuke.Script_Knob('clearBuffers','Clear Buffers')
    self.addKnob(self.clearBuffers) 
	
    self.bufferReport = nuke.nuke.Multiline_Eval_String_Knob( "bufferReport", "Buffer Report" )
    self.addKnob(self.bufferReport)
    self.bufferReport.setValue(str(nukescripts.cache_report(str())))	


    # Initially populate the Sliders...
    updateSliders(self)

  
  def knobChanged(self,knob):
  
    if knob == self.updateButton:
      updateSliders(self)
      
    elif knob == self.clearCacheButton:
      nuke.clearDiskCache()
      # Re-populate the Sliders...
      updateSliders(self)

      print 'Disk cache cleared.'
        
    elif knob == self.clearBuffers:
	  nukescripts.cache_clear("")
	  self.bufferReport.setValue(str(nukescripts.cache_report(str())))
	  print 'Buffers cleared.'

def addPanel():
  return DiskCachePanel().addToPane()

def getCachePerc():
  folder = nuke.toNode('preferences').knob('DiskCachePath').value()
  cachedBytes = 0
  for (path, dirs, files) in os.walk(folder):
    for file in files:
      filename = os.path.join(path, file)
      cachedBytes += os.path.getsize(filename)
  # Work out the Cache Limit set in Bytes
  totalCacheGB = nuke.toNode('preferences').knob('diskCacheGB').value()
  totalCacheBytes = totalCacheGB*pow(1024,3)
  # Percentage Cache Used
  cacheUsed = (cachedBytes/totalCacheBytes)*100
  return cacheUsed

# For Calculating the Disk Cache
def getDiskCachePerc6():
  
  # Get Preference Settings
  totalDiskCacheGB = nuke.toNode('preferences').knob('diskCacheGB').value()
  totalPaintCacheGB = nuke.toNode('preferences').knob('PaintCacheGB').value()
  
  diskCacheDir = nuke.toNode('preferences').knob('DiskCachePath').value()
  tileCacheDir = nuke.toNode('preferences').knob('DiskCachePath').value() + "/tilecache"
  if (diskCacheDir.find("getenv") != -1):
    diskCacheDir = os.environ['NUKE_TEMP_DIR']
    tileCacheDir = os.environ['NUKE_TEMP_DIR'] + "/tilecache"
  
  # DiskCache
  diskCachedBytes = 0
  for (path, dirs, files) in os.walk(diskCacheDir):
    for file in files:
      filename = os.path.join(path, file)
      diskCachedBytes += os.path.getsize(filename)
      
  paintCachedBytes = 0
  for (path, dirs, files) in os.walk(tileCacheDir):
    for file in files:
      filename = os.path.join(path, file)
      paintCachedBytes += os.path.getsize(filename)   
 
  # Work out the Cache Limit set in Bytes
  totalDiskCacheBytes = totalDiskCacheGB*pow(1024,3)
  # Percentage Cache Used
  diskCachePerc = ((diskCachedBytes-paintCachedBytes)/totalDiskCacheBytes)*100

  # Work out the Cache Limit set in Bytes
  totalPaintCacheBytes = totalPaintCacheGB*pow(1024,3)
  # Percentage Cache Used
  paintCachePerc = (paintCachedBytes/totalPaintCacheBytes)*100
  
  return diskCachePerc, paintCachePerc
  
  
  
def getDiskCachePerc5():
  
  # Get Preference Settings
  totalDiskCacheGB = nuke.toNode('preferences').knob('diskCacheGB').value()
    
  diskCacheDir = nuke.toNode('preferences').knob('DiskCachePath').value()
  tileCacheDir = nuke.toNode('preferences').knob('DiskCachePath').value() + "/tilecache"
  if (diskCacheDir.find("getenv") != -1):
    diskCacheDir = os.environ['NUKE_TEMP_DIR']
    tileCacheDir = os.environ['NUKE_TEMP_DIR'] + "/tilecache"
    
    
  # DiskCache
  diskCachedBytes = 0
  for (path, dirs, files) in os.walk(diskCacheDir):
    for file in files:
      filename = os.path.join(path, file)
      diskCachedBytes += os.path.getsize(filename)
      
  paintCachedBytes = 0
  for (path, dirs, files) in os.walk(tileCacheDir):
    for file in files:
      filename = os.path.join(path, file)
      paintCachedBytes += os.path.getsize(filename)   
      
  
      
  # Work out the Cache Limit set in Bytes
  totalDiskCacheBytes = totalDiskCacheGB*pow(1024,3)
  # Percentage Cache Used
  diskCachePerc = ((diskCachedBytes-paintCachedBytes)/totalDiskCacheBytes)*100
  
  return diskCachePerc
  

# Method to update the sliders
def updateSliders(self):
  self.bufferReport.setValue(str(nukescripts.cache_report(str())))  
  if nuke.env['NukeVersionMajor']==5:
    percs = getDiskCachePerc5()
    self.diskCachePercUsed.setValue(percs)
  else:
    percs = getDiskCachePerc6()
    self.diskCachePercUsed.setValue(percs[0])
    self.paintCachePercUsed.setValue(percs[1]) 


  
#menu = nuke.menu('Pane')
#menu.addCommand('DiskCache',addPanel)
#nukescripts.registerPanel('uk.co.thefoundry.DiskCache', addPanel)

nuke.menu('Pane').addCommand('DiskCache', addPanel)
nukescripts.registerPanel('uk.co.thefoundry.DiskCache', addPanel)