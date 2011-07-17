#Frank Rüter
# converts a range to a list
# aRange == "1,2,5-10,30-35x5"

proc rangeToListSimple {aRange} {
   set theList ""
   foreach cur_item [split $aRange ","] {
	set rangeAndBy [split [string trim $cur_item] "x"]
	set range [lindex $rangeAndBy 0]
	set by [lindex $rangeAndBy 1]
	if {$by == ""} { set by 1 }
	set limits [split $range "-"]
	set start [lindex $limits 0]
	#if [info exists end] {unset end}
	set end  [lindex $limits 1]
	if {$end != ""} {
		for {set i $start} {$i <= $end} {incr i $by} {
			lappend theList $i
			}
		} else {
		lappend theList $start
		}
	}
return $theList
}
