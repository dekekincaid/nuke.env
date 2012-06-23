proc submit_bugzilla {} {
    global env
    global WIN32
    global version_long
    
    if [catch {set nodelist [selected_nodes]}] {set nodelist ""}
    
    foreach n $nodelist {
        lappend namelist [knob $n.name]
    }
    
    set ver [lindex [split [lindex $version_long 0] .] 2]
    set severity {Unsure}
    
    if { $ver>10} {
        if [catch {
            panel "Submit nuke report" {
                {
                    "Severity" severity e {
                        {Enhancement - request for enhancement}
                        {Trivial - cosmetic problem like misspelled words or misaligned text}
                        {Minor - minor loss of function, or problem where reasonable workaround exists}
                        {Unsure}
                        {Major - major loss of function}
                        {Critical - crash or loss of data}
                        {Blocker - blocks production}
                    }   
                }
            {"Component" component e {
                3d
                Architecture
                Bezier
                Cache
                Channel
                Color
                "Curve Editor"
                DAG
                "Distort / Warp"
                Documentation
                Draw
                "File I/O"
                Filter
                Flipbook
                General
                "Group & Gizmo"
                Image
                Keyer
                Merge
                OFX
                Paint
                "Panel UI"
                Plugins
                Preferences
                Race
                "Scan Line Renderer"
                Time
                Tracker
                Transform
                Viewer }}
           {"Short Description" shortdesc}
           {"Full Description" fulldesc n}
           {"CC" cclist}
           {"Problem nodes" namelist}
        }
    }] return;
   } else {
   if [catch {
        panel "Submit nuke report" { {"Feature Request" feature b} {"Short Description" shortdesc} {"Full Description" fulldesc n} {"CC" cclist} {"Problem nodes" namelist}}
    }] return;
   }

   # Fix the "severity" field to match what Bugzilla is expecting
   set space_index [string first { } $severity]
   if $space_index!=-1 {
       incr space_index -1
       set new_sev [string range $severity 0 $space_index]
   } else {
       set new_sev $severity
   }
   set severity [string tolower $new_sev]
   if {[string match $severity {unsure}]==1} { set severity "normal" }

set mailserversocket [socket mail.thefoundry.co.uk 25]
fconfigure $mailserversocket -buffering line
puts $mailserversocket "mail from: $env(USER)@d2.com"
puts $mailserversocket "rcpt to: bugzilla@d2.com"
puts $mailserversocket "data"
puts $mailserversocket "From: $env(USER)@d2.com"
puts $mailserversocket "To: bugzilla@d2.com <bugzilla@d2.com>"
puts $mailserversocket "Subject: $shortdesc"
puts $mailserversocket ""
puts $mailserversocket "@product = NUKE"
puts $mailserversocket "@version = 4.5"
if {$ver>10} {
   puts $mailserversocket "@component = $component"
} else {
   puts $mailserversocket "@component = general"
}
puts $mailserversocket "@rep_platform = All"
puts $mailserversocket "@cc = $cclist"
puts $mailserversocket "@groupset = DD"
  
if { $WIN32 } {
    puts $mailserversocket "@op_sys = Windows 2000"
} else {
    catch {
        if {$env(HOSTTYPE) == "Linux"} {
            puts $mailserversocket "@op_sys = Linux"
        }
        if {$env(HOSTTYPE) == "IRIX64"} {
            puts $mailserversocket "@op_sys = IRIX"
        }
        if {$env(HOSTTYPE) == "IRIX32"} {
            puts $mailserversocket "@op_sys = IRIX"
        }
        if {$env(HOSTTYPE) == "IRIX"} {
            puts $mailserversocket "@op_sys = IRIX"
        }
    }
}
puts $mailserversocket "@priority = P5"
puts $mailserversocket "@bug_severity = $severity"
puts $mailserversocket ""
puts $mailserversocket "VERS:   $version_long"
catch {puts $mailserversocket "HOST:   $env(HOST)"}
catch {puts $mailserversocket "HOSTOS: $env(HOSTTYPE)"}
catch {puts $mailserversocket "USER:   $env(USER)"}
catch {puts $mailserversocket "JOB:    $env(JOB)"}
catch {puts $mailserversocket "SHOT:   $env(SHOT)"}
  
set script [knob root.name]
  
if ![regexp {^/|^.:} $script] {
    if [info exists env(PWD)] {
        set script $env(PWD)/$script
    } elseif !$WIN32 {
    set script [pwd]/$script
    }
}
  
if $WIN32 {
    regsub {^.:} $script "" script
    regsub -all {\\} $script "/" script
} else {
    regsub {^/tmp_mnt} $script "" script
    regsub {^/export} $script "" script
}
  
puts $mailserversocket "SCRIPT: $script"
puts $mailserversocket "NODES:  $namelist"
puts $mailserversocket ""
puts $mailserversocket "$fulldesc"
puts $mailserversocket "."
flush $mailserversocket
gets $mailserversocket
gets $mailserversocket
gets $mailserversocket
gets $mailserversocket
gets $mailserversocket result
alert $result
close $mailserversocket
  
}

