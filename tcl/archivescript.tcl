#
# Copyright (c) 2003 Digital Domain Inc.  All Rights Reserved.
#
# take the image inputs of a script and archive them and change the iread information so that the script can be easily ported
#

proc archivescript {} {
global destpath
set framerangefirst [value root.first_frame]
set framerangelast [value root.last_frame]

set readnos 0
set objnos 0
if [catch {
panel "Script Archiver" {
    {"Destination Path" destpath f2}
    {"First frame for archive" framerangefirst}
    {"Last frame for archive" framerangelast}
  }
}

    # use this if we wanna mess with proxy too.  feh.
    #{"Output Proxy?" outputproxy b}
   ] {message "Cancelled Operation"} else {
    # this is where the process goes
    
    # check to see if destination path is valid
    if ![file exists $destpath] {
        error "Path does not exist :\n$destpath"
        } else {
            puts "\n---Archiving Script : [value root.name]\n---\n"
            foreach n [nodes] {
                if {[class $n]=="Read"} {
                    set readdir [dirname [filename $n]]
                    set dirtomake $destpath[file tail $readdir]
                    
                    incr readnos
                    if {[value root.first_frame] == $framerangefirst && [value root.last_frame] == $framerangelast} {
                    puts "  Archiving directory : $readdir"
                    file copy $readdir $dirtomake
                    } else {
                    puts "---Creating archive dir $dirtomake\n"
                    file mkdir $dirtomake
                    for {set x $framerangefirst} {$x<=$framerangelast} {incr x} {
                        puts "  Archiving : [format [filename $n] $x]\n"
                        file copy [format [filename $n] $x] $dirtomake/[file tail [format [filename $n] $x]]
                    }
                    }
                    if ![knob root.proxy] {
                        knob $n.file $dirtomake/[basename [filename $n]]
                    } else {
                        knob $n.proxy $dirtomake/[basename [filename $n]]
                    }
                }
            }
        }
        puts "\nArchiving Done"
        message "Script archived\n$readnos image inputs archived.\n"
    }
}

