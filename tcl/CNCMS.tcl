#copyright florian strobl
#CineNuke Fake for Nuke 
#brings in the LUT for Shake into Nuke


proc CNCMS {SHAKELUT } {

	
global env
set n 0
set x ""
set f ""
set valuered ""
set valuegreen ""
set valueblue ""
set no ""



knob root.transfer linear


#set computername [string tolower $COMPUTERNAME]

set x  [expression 1/1023]
set f [open $SHAKELUT r]

  
set n 0

while {[eof $f] != 1 } {
        gets $f line
	puts "[llength $line]"
	set div 1023
	if {[llength $line] == 3} {
	set a  [expr [lindex $line 0]/$div] 
	set b  [expr [lindex $line 1]/$div] 
	set c  [expr [lindex $line 2]/$div]
	
	append valuered "x[expression $x*$n]  $a "     
	append valuegreen "x[expression $x*$n]  $b "
	append valueblue  "x[expression $x*$n] $c " 
	incr n

	}


}
close $f
set redpass "curve $valuered"
set greenpass "curve $valuegreen"
set bluepass "curve $valueblue"
     
push 0
ColorLookup "
 channels {rgba.red rgba.green rgba.blue -rgba.alpha}
   lut {master {curve C 0 1}
       red {$redpass}
       green {$greenpass}
       blue {$bluepass}
       }
   name VIEWER_INPUT
"
}




