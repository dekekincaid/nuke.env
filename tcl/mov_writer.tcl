# mov writer 
# a script to run with the to-mov tool
# © mov@cgpolis.com

proc $movwriterdir/mov_writer {} {
global movwriterdir

set self [knob name]

if {[knob $self.scene]=="" && [knob $self.pal]=="true"} {     
        error "Please get or enter a valid scene name"
}                                                     

set n [selected_node]
set nfilename [filename $n]
if {$nfilename==""} {
     knob $self.icon $movwriterdir/cgpdot.xpm
     error "please select READ or WRITE node with a valid file_name"
}
set ifwrite 0
if {[class $n]=="Write"} {
     set ifwrite 1
     Read -New [list file $nfilename name Temp_Read selected true]
     foreach n [selected_nodes] {
     knob $n.tile_color 0xff000000
     knob $n.postage_stamp false
     knob $n.first [knob root.first_frame]
     knob $n.last [knob root.last_frame]
     }
}
set range [knob $n.first],[knob $n.last]
if {$ifwrite=="1"} {
      node_copy [cut_paste_file]
      node_delete
}
# framerange
if {[knob range]=="false"} {
    if [catch {set r [get_input "Frames to execute:" $range]}] return
    set range $r
}
#range stuff
set firstrc [string first , $range]
if {$firstrc=="-1"} {
set rangef $range
set rangel $range
} else {
  set rangelength [string length $range]
  set rangef [string range $range 0 [expr $firstrc-1]]
  set rangel [string range $range [expr $firstrc+1] $rangelength]
  }
set rangefclass [string is digit $rangef]
set rangelclass [string is digit $rangel]
if {$rangefclass=="0" || $rangelclass=="0"} {
knob $self.icon $movwriterdir/cgpdot.xpm
error "please enter a correct framerange (digits)"
}
#
if {$ifwrite=="1"} {
    node_paste [cut_paste_file]
    set tempreadnode [selected_node]
     foreach n [selected_nodes] {
     knob $n.first $rangef
     knob $n.last $rangel
     }
}
set readnode [selected_node]
set readfile [filename $n]
set textpath [file dirname [knob text_path]a]/
set cleanpath [file dirname [knob clean_path]a]/
set readdirname [file dirname $readfile]
set dirname [file dirname $readdirname]
file mkdir $dirname/temp
set tempdir $dirname/temp
set filetail [file tail $readfile] 
set temptif $tempdir/$filetail
set strlen [string length [file dirname $readfile]]
set rstrlen [string length $readfile]
if {[knob fignore]=="false"} {
            set seqname [string range $readfile [expr $strlen +1] [expr $rstrlen-10]]_[knob txt_n]
            } else {
set seqname [knob txt_n]
}
if {[knob pathov]=="true"} {
            set dirname $textpath
            set dircheck [file isdirectory $dirname]
                    if {$dircheck=="0"} {
                       knob $self.icon $movwriterdir/cgpdot.xpm                    
                       error "please enter a valid dir for text mov output"
                    }
}
set movfilename $dirname/$seqname.mov
set textdir $dirname
###############################################################temp tif
knob $readnode.selected true
if {[knob $self.pathov]=="true"} {
        set dirname $cleanpath
        set dircheck [file isdirectory $dirname]
        if {$dircheck=="0"} {
	    knob $self.icon $movwriterdir/cgpdot.xpm        
          error "please enter a valid dir for clean mov output"
        }
}
Reformat -New
foreach n [selected_nodes] {
        knob $n.proxy_format [knob $self.format]
        knob $n.to [knob $self.format]
        knob $n.tile_color 0xff000000
        knob $n.crop true
}
set reformatnode [stack 0]
Crop -New
foreach n [selected_nodes] {
       knob $n.tile_color 0xff000000
}
set cropnode [stack 0]
Write -New [list file $temptif name temp_tif selected true]
foreach n [selected_nodes] {
       #knob $n.file_type exr
       #knob $n.datatype "16 bit half"
       knob $n.file_type tif
       knob $n.datatype "8 bit"
       knob $n.tile_color 0xff000000
       knob $n.compression none
}
set executenode [stack 0]

               ##############################group
               foreach n [nodes] {knob $n.selected false}
               knob $executenode.selected true
               knob $reformatnode.selected true
               knob $cropnode.selected true
               set rx [knob $readnode.xpos]
               set ry [knob $readnode.ypos]
               # copy operation
               node_copy [cut_paste_file]
               node_delete
               # create a new group and select it
               Group " selected true
               tile_color 0xff000000
               name temp_tif
               	xpos $rx
               	ypos [expr $ry+100]
               	"
               set groupnode [stack 0]
               Input -New
               # paste the nodes in
               node_paste [cut_paste_file]
               set executenode [stack 0]
               input $groupnode 0 $readnode
                                    
               ########################## end group
if [catch {               
               knob $self.icon $movwriterdir/cgpdot2.xpm               
               execute $executenode $range
               end_group                                           
foreach n [nodes] {knob $n.selected false}
               knob $groupnode.selected true
               node_delete
                                 if {$ifwrite=="1"} {
                                     knob $tempreadnode.selected true
                                     node_delete
                                 }      
               } errormsg] {
                              if {[knob $self.log]=="true"} {
                              set log [open $dirname/MovLog.txt a+]
                              set timestamp [clock format [clock seconds]]
                              puts $log "!warning, cancelled, $timestamp "
                              close $log
                              }
              end_group 
                                 if {$ifwrite=="1"} {
                                     knob $tempreadnode.selected true
                                     node_delete
                                 }
               foreach n [nodes] {knob $n.selected false}
                     catch {           
                     knob $groupnode.selected true
                     node_delete               
                     }
               file delete -force $tempdir
               knob $self.icon $movwriterdir/cgpdot.xpm
               return {}                            
               }

Read -New [list file $temptif name Temp_Read selected true]
     foreach n [selected_nodes] {
     knob $n.tile_color 0xff000000
     knob $n.postage_stamp false
     knob $n.first $rangef
     knob $n.last $rangel
     }
set readnode [stack 0]
set temptifreadnode [stack 0]

###############################################################PAL_CLEAN
foreach n [nodes] {knob $n.selected false}
knob $readnode.selected true
if {[knob $self.fignore]=="false"} {
       set seqname [string range $readfile [expr $strlen +1] [expr $rstrlen-10]]_[knob $self.cln_n]
       } else {
       set seqname [knob $self.cln_n]
}
set movfilename2 $dirname/$seqname.mov
set cleandir $dirname
Write -New [list file $movfilename2 name mov_output selected true]
foreach n [selected_nodes] {
       knob $n.file_type "mov"
       knob $n.codec [knob $self.codec]
       knob $n.fps [knob $self.fps]
       knob $n.quality [knob $self.quality]
       knob $n.tile_color 0xff000000
}
set executenode [stack 0]
if {[knob $self.clean]=="false"} {
       knob $executenode.selected true
       node_delete
}
if {[knob $self.clean]=="true"} {
       if {[knob $self.log]=="true"} {
       set log [open $dirname/MovLog.txt a+]
       set timestamp [clock format [clock seconds]]
       puts $log " "
       puts $log "____ "
       puts $log "$timestamp "
       puts $log " "
       puts $log "Incoming sequence: $readfile"
       puts $log "scene: [knob $self.scene]"
       puts $log " "
       puts $log "wrote clean_mov: $movfilename2; $range frames"
       puts $log "regards, NUKE "
       close $log
       } 
               if [catch {
               ##############################group
               foreach n [nodes] {knob $n.selected false}
               knob $executenode.selected true
               set rx [knob $readnode.xpos]
               set ry [knob $readnode.ypos]
               # copy operation
               node_copy [cut_paste_file]
               node_delete
               # create a new group and select it
               Group " selected true
               tile_color 0xff000000
               name to_MOV_clean
               	xpos $rx
               	ypos [expr $ry+100]
               	"
               set groupnode [stack 0]
               Input -New
               # paste the nodes in
               node_paste [cut_paste_file]
               set executenode [stack 0]
               input $groupnode 0 $readnode
               ########################## end group
               execute $executenode $range
               end_group                              
               foreach n [nodes] {knob $n.selected false}
               knob $groupnode.selected true
               node_delete
               } errormsg] {
                              if {[knob $self.log]=="true"} {
                              set log [open $dirname/MovLog.txt a+]
                              set timestamp [clock format [clock seconds]]
                              puts $log "!warning, cancelled, $timestamp "
                              close $log
                              }
               end_group                              
               foreach n [nodes] {knob $n.selected false}
               knob $groupnode.selected true
               knob $temptifreadnode.selected true
               node_delete
               knob $self.icon $movwriterdir/cgpdot.xpm
               file delete -force $tempdir
               return {}
               }
}
#END PAL_clean]
###############################################################PAL
knob $readnode.selected true
Text -New
foreach n [selected_nodes] {
        knob $n.message "[knob $self.scene]"
        knob $n.font "[knob $self.font]" 
        knob $n.translate "15 15" 
        knob $n.size [knob $self.size]
        set colorr [knob $self.fcolor.r]
        set colorg [knob $self.fcolor.g]
        set colorb [knob $self.fcolor.b] 
        set color "$colorr $colorg $colorb 1"
        knob $n.color $color
        knob $n.tile_color 0xff000000
}
set text1node [stack 0]
set formatfirstp [string first " " [knob $self.format]]
set formatwidth [string range  [knob $self.format] 0 [expr $formatfirstp-1]]
Text -New
foreach n [selected_nodes] {
        if {[knob $self.framecode]=="true"} {
                 if {[knob $self.tcframe]==""} {
                alert "You've selected to change the framecode without first frame value, I'll use 0"
                knob $n.message "Frame:\[\expr \[frame\]-$rangef\]"
                } else {
                 set strclass [string is digit [knob $self.tcframe]]                           
                      if {$strclass=="0"} {
                                knob $text1node.selected true
                                knob $temptifreadnode.selected true
                                node_delete
                                file delete -force $tempdir
                                knob $self.icon $movwriterdir/cgpdot.xpm
                                error "please enter a valid frame number in the \"framecode first frame\" field. Valid frames contain only digits."
                                } else {
                      knob $n.message "Frame:\[\expr \[frame\]-$rangef+[knob $self.tcframe]\]"
                      }
                }
    } else {
    knob $n.message "Frame:\[frame\]"
    }
        knob $n.font "[knob $self.font]"
        set colorr [knob $self.fcolor.r]
        set colorg [knob $self.fcolor.g]
        set colorb [knob $self.fcolor.b] 
        set color "$colorr $colorg $colorb 1"
        knob $n.color $color
        knob $n.translate "[expr $formatwidth-15] 15" 
        knob $n.size [knob $self.size]
        knob $n.xjustify "right"
        knob $n.tile_color 0xff000000
}
set text2node [stack 0]
Write -New [list file $movfilename name mov_output selected true]
foreach n [selected_nodes] {
        knob $n.file_type "mov"
        knob $n.codec [knob $self.codec]
        knob $n.fps [knob $self.fps]
        knob $n.quality [knob $self.quality]
        knob $n.tile_color 0xff000000
}
set executenode [stack 0]

        if [catch {
                if {[knob $self.pal]=="true"} {
                if {[knob $self.log]=="true"} {
                set log [open $textdir/MovLog.txt a+]
                set timestamp [clock format [clock seconds]]
                puts $log " "
                puts $log "____ "
                puts $log "$timestamp "
                puts $log " "
                puts $log "Incoming sequence: $readfile"
                puts $log "scene: [knob $self.scene]"
                puts $log " "
                puts $log "wrote text_mov: $movfilename; $range frames"
                puts $log "regards, NUKE "
                close $log
                }
                }
                ##############################group
                foreach n [nodes] {knob $n.selected false}
                knob $executenode.selected true
                knob $text1node.selected true
                knob $text2node.selected true
                set rx [knob $readnode.xpos]
                set ry [knob $readnode.ypos]
                node_copy [cut_paste_file]
                node_delete
                Group " selected true
                tile_color 0xff000000
                name to_MOV_text
        	xpos $rx
        	ypos [expr $ry+100]
        	"
                set groupnode [stack 0]
                Input -New
                node_paste [cut_paste_file]
                set executenode [stack 0]
                input $groupnode 0 $readnode
                ########################## end group
                                if {[knob $self.pal]=="true"} {
                                        execute $executenode $range
                                }
                end_group                              
                foreach n [nodes] {knob $n.selected false}
                knob $groupnode.selected true
                knob $temptifreadnode.selected true
                node_delete               
                                 
                } errormsg] {
                end_group                              
                foreach n [nodes] {knob $n.selected false}
                knob $groupnode.selected true
                knob $temptifreadnode.selected true
                node_delete
                                if {[knob $self.log]=="true"} {
                                                set log [open $dirname/MovLog.txt a+]
                                                set timestamp [clock format [clock seconds]]
                                                puts $log "!warning, cancelled, $timestamp "
                                                close $log
                                }
                 knob $self.icon $movwriterdir/cgpdot.xpm
                 file delete -force $tempdir
                 return {}
                 }

file delete -force $tempdir
################################### open in
set cleandir [file dirname $cleandir/a]
set textdir [file dirname $textdir/a]
set textdir [regsub -all "\/" $textdir "\\"]
set cleandir [regsub -all "\/" $cleandir "\\"]

if {[knob $self.pal]=="true"} {
               set dirName $textdir
} else {
             set dirName $cleandir
}                                   

if {[knob $self.exp]=="true"} {
    if {[knob $self.br]=="explorer"} {
    exec explorer.exe $dirName &
    } else {
          exec [knob $self.totalcmd] $dirName &
      }
}
knob $self.icon $movwriterdir/cgpdot.xpm
return {}
}