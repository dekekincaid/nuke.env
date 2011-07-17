#This script will Create Directories for all Write nodes in your script.
#Written by Ryan Trippensee 10.15.08

proc CreateDirectories {} {

set g {
Directories Created!
}

foreach n [nodes] {
  if {[class $n]=="Write"} {
  file mkdir "[file dirname [value  $n.file]]"
  }
 }

message $g

}
