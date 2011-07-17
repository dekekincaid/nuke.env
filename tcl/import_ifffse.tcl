# Copyright (c) 2008 Timur Saitgaraev aka_tt@mail.ru
# this helps to import Imagineer systems Mocha tracking data via IFFFSE Point Tracker Data format
# This is what is executed by the Animation File/Import/Ascii.. menu item

proc import_ifffse {} {
	global ascii_filename
	set astart [knob root.first_frame]
	
	set args {{"File:" ascii_filename f} {"Start at:" astart}}
	    if [catch {panel "Import Mocha" $args}] return
	    
	set InChan [open $ascii_filename]; 
	set MoTr1 [read $InChan];   
	close $InChan
	
	set cl [lrange [split [regsub -all {,\s+} [regsub -all {\s+\d+\.?\d*\s+:\s+} $MoTr1 "\n"] "\t"] \n] 1 end-1]
	set animations [animations]
	
	
		animation this.x erase -100000000 100000000
		animation this.y erase -100000000 100000000
		for {set x 0} {$x < [llength $cl]} {incr x} {
			split [lindex $cl $x] \t
			setkey this.x $astart+$x [lindex [split [lindex $cl $x] \t] 0]
			setkey this.y $astart+$x [lindex [split [lindex $cl $x] \t] 1]
			}
		}
}