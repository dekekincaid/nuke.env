###########################################################
# SubmitNukeToDeadline.tcl
# Ryan Russell (Prime Focus), 2006
#
# Integrated Nuke tcl script to submit jobs to Deadline.
###########################################################

###########################################################
# Helper Procedures
###########################################################

# Opposite of incr.
proc decr {varName {decrement 1}} {
	upvar 1 $varName var
	incr var [expr {-$decrement}]
}

# Checks if the value is a valid Integer.
proc IsInteger { value } {
	if { [regexp {^[0-9]+$} $value] > 0 } {
		return true
	}
	return false
}

# Checks if the value is a valid Boolean.
proc IsBoolean { value } {
	set value [string tolower $value]

	if { [string compare $value "0"] == 0 || [string compare $value "1"] == 0 || [string compare $value "true"] == 0 || [string compare $value "false"] == 0 } {
		return true
	}
	return false
}

# Checks if the given filename ends with a movie extension
proc IsMovie { path } {
	set ext [file extension $path]
	if {[string compare -nocase $ext ".mov"] == 0} {
		return true
	}
	return false
}

# Gets the chunk size that is required if submitting a movie job.
proc GetChunkSize { defaultValue } {
	set theNodes [nodes]
	foreach node $theNodes {
		if {[class $node] == "Write" && [knob $node.disable] != true } {
			if {[IsMovie [filename $node]]} {
				return 1000000
			}
		}
	}
	return $defaultValue
}

# Gets the chunk size that is required for a particular write node.
proc GetChunkSizeForWriteNode { writeNodeName defaultValue } {
	set theNodes [nodes]
	foreach node $theNodes {
		if {[class $node] == "Write" && [knob $node.name] == $writeNodeName } {
			if {[IsMovie [filename $node]]} {
				return 1000000
			}
			return $defaultValue
		}
	}
	return $defaultValue
}

# Checks if path is local (c, d, or e drive).
proc IsPathLocal { path } {
	if {[string compare -nocase -length 2 $path "c:"] == 0 || [string compare -nocase -length 2 $path "d:"] == 0 || [string compare -nocase -length 2 $path "e:"] == 0 } {
		return true
	}
	return false
}

# Checks if the filename is padded (ie: \\output\path\filename_%04.tga).
proc IsFilenamePadded { filename } {
	global nuke_version_major
	global nuke_version_minor

	if {[regexp "\%(\[0-9\]+)d" $filename match count] == 1} {
		return true
	} elseif { $nuke_version_major >= 5 && $nuke_version_minor >= 1 && [string first "#" $filename] > -1 } {
		return true
	}
	return false
}

# Parses through the filename looking for the first padded pattern, replaces
# it with the correct number of #'s, and returns the new padded filename.
proc GetPaddedFilename { filename } {
	# Only the first pattern is replaced by Nuke.
	if {[regexp "\%(\[0-9\]+)d" $filename match count] == 1} {
		# Removes any leading zeros.
		incr count 0
		
		# Create the padding string.
		set padding ""
		while {$count > 0} {
			set padding "$padding#"
			decr count
		}
		
		# Replace the pattern with the padded string.
		regsub "\%\[0-9\]+d" $filename $padding filename
	}
	
	# Return the padded filename.
	return $filename
}

# Check all the paths and warn user if any are local or not padded.
proc CheckFilePaths { submitScript } {
	set theNodes [nodes]
	set warningMessages ""
	
	# Warn if there are no outputs.
	set outputCount 0
	foreach node $theNodes {
		if {[class $node] == "Write" && [knob $node.disable] != true } {
			incr outputCount
		}
	}
	if {$outputCount == 0} {
		set warning "THERE ARE NO ENABLED WRITE NODES !!"
		set warningMessages $warningMessages$warning
	}

	# Check all the output filenames if they are local or not padded (non-movie files only).
	foreach node $theNodes {
		if {[class $node] == "Write" && [knob $node.disable] != true } {
			if {[IsPathLocal [filename $node]]} {
				set warning "Output path \"[filename $node]\" is local.\n"
				set warningMessages $warningMessages$warning
			}
			
			if {![IsMovie [filename $node]] && ![IsFilenamePadded [filename $node]]} {
				set warning "Output path \"[filename $node]\" is not padded.\n"
				set warningMessages $warningMessages$warning
			}
		}
	}

	# Check if the script file is local and not being submitted to Deadline.
	if {! $submitScript} {
		if {[IsPathLocal [knob root.name]]} {
			set warning "Script path \"[knob root.name]\" is local and is not being submitted to Deadline.\n"
			set warningMessages $warningMessages$warning
		}
	}
	
	# If there are any warning messages, show them to the user.
	if {[string length $warningMessages] > 0 } {
		if {[catch {
			panel "Submission Warnings" {
				{Warnings: warningMessages n }
				{"Do you still wish to submit this job to Deadline?"}
			}
		} result]} { 
			return false
		}
	}
	
	return true
}

# Gets a Deadline array and returns them it as a string
proc GetDeadlineArrayString { argument } {
	global env
	global WIN32
	
	set tempPath ""
	if {$WIN32} {
		set tempPath $env(TEMP)
	} else {
		set tempPath "/tmp"
	}
	
	set outputFilename "$tempPath/output.txt"
	set exitCodeFilename "$tempPath/exitCode.txt"

	# Query Deadline.
	#exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $argument
	if {[file exists "/Applications/Deadline/Resources/bin/deadlinecommandbg"] == 1} {
		exec "/Applications/Deadline/Resources/bin/deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $argument
	} else {
		exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $argument
	}
	
	# Open the file and read in the results.
	set arrayString ""
	catch {set fileid [open $outputFilename r]}
	while {[gets $fileid line] >= 0} {
		set arrayString [concat $arrayString "\"$line\""]
	}
	close $fileid
	
	# Return the array string.
	return $arrayString
}

# Get the settings config filename.
proc GetSettingsFilename {} {
	global env
	global WIN32
	
	set tempPath ""
	if {$WIN32} {
		set tempPath $env(TEMP)
	} else {
		set tempPath "/tmp"
	}
	
	set outputFilename "$tempPath/output.txt"
	set exitCodeFilename "$tempPath/exitCode.txt"

	# Query Deadline.
	#exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename "-getsettingsdirectory"
	if {[file exists "/Applications/Deadline/Resources/bin/deadlinecommandbg"] == 1} {
		exec "/Applications/Deadline/Resources/bin/deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename "-getsettingsdirectory"
	} else {
		exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename "-getsettingsdirectory"
	}
	
	# Open the file and read the first line.
	catch {set fileid [open $outputFilename r]}
	gets $fileid settingsRoot
	close $fileid
	
	set settingsFilename [file join $settingsRoot "NukeDeadlineConfig.ini"]
	return $settingsFilename
}

###########################################################
# Main Script
###########################################################

# Some global variables.
global env
global nuke_version_major
global WIN32

set tempPath ""
if {$WIN32} {
	set tempPath $env(TEMP)
} else {
	set tempPath "/tmp"
}
	
# Save the file in case the user hasn't done it.
script_save [knob root.name]

# Filenames to use.
set outputFilename "$tempPath/output.txt"
set exitCodeFilename "$tempPath/exitCode.txt"

set submitInfoFile "$tempPath/nuke_submit_info.job"
set pluginInfoFile "$tempPath/nuke_plugin_info.job"
set deadlineTempTclFile "$tempPath/TempSubmitToDeadline.tcl"

set deadlineConfigFile [GetSettingsFilename]

# Get the nodes.
set theNodes [nodes]

# Get the Deadline arrays.
set groups [GetDeadlineArrayString "-groups"]
set pools [GetDeadlineArrayString "-pools"]

set onJobCompletes ""
set onJobCompletes [concat $onJobCompletes "\"Nothing\""]
set onJobCompletes [concat $onJobCompletes "\"Archive\""]
set onJobCompletes [concat $onJobCompletes "\"Delete\""]

set builds ""
set builds [concat $builds "\"None\""]
set builds [concat $builds "\"32bit\""]
set builds [concat $builds "\"64bit\""]

# Set the job name and frame range default values.
set jobName [file tail [knob root.name]]
set frames "[knob root.first_frame]-[knob root.last_frame]"

# Set the other default values.
set comment ""
set taskTimeout "0"
set threadCount 0
set ramUsage 0

# Set the default for these sticky settings.
set department ""
set group "none"
set pool "none"
set build "None"
set priority "50"
set machineLimit "0"
set chunkSize 1
set submitSuspended false
set onJobComplete "Nothing"
set submitScript 1
set separateJobs false

# Try to read in the sticky settings.
catch { 
	set fileid [open $deadlineConfigFile r]
	
	# First read in the sticky settings.
	gets $fileid initDepartment
	gets $fileid initGroup
	gets $fileid initPool
	gets $fileid initPriority
	gets $fileid initMachineLimit
	gets $fileid initChunkSize
	gets $fileid initSubmitSuspended
	gets $fileid initSubmitScript
	gets $fileid initLimitGroup
	gets $fileid initSeparateJobs
	close $fileid
	
	# Now set them if no error occurred while reading.
	set department $initDepartment
	set group $initGroup
	set pool $initPool
	set limitGroup $initLimitGroup
	
	if {[IsInteger $initPriority]} {
		set priority $initPriority
	}
	if {[IsInteger $initMachineLimit]} {
		set machineLimit $initMachineLimit
	}
	if {[IsInteger $initChunkSize]} {
		set chunkSize $initChunkSize
	}
	if {[IsBoolean $initSubmitSuspended]} {
		set submitSuspended $initSubmitSuspended
	}
	if {[IsBoolean $initSubmitScript]} {
		set submitScript $initSubmitScript
	}
	if {[IsBoolean $initSeparateJobs]} {
		set separateJobs $initSeparateJobs
	}
}

set errors true
while { $errors } {
	set errors false
	
	# Dynamically create the actual submission dialog. This was the only
	# way I could figure out to set the pools and group combo boxes.
	catch {set fileid [open $deadlineTempTclFile w]}
	puts $fileid "panel -w500 \"Submit Nuke To Deadline\" {"
	puts $fileid "  { \"Job Name\" jobName }"
	puts $fileid "  { \"Comment\" comment }"
	puts $fileid "  { \"Department\" department }"
	puts $fileid "  { \"Pool\" pool e { $pools } }"
	puts $fileid "  { \"Group\" group e { $groups } }"
	puts $fileid "  { \"Priority (0 to 100)\" priority x}"
	puts $fileid "  { \"Machine Limit (0 for no limit)\" machineLimit x}"
	puts $fileid "  { \"Task Timeout (0 for no timeout)\" taskTimeout x}"
	puts $fileid "  { \"Limit Groups (separate with commas)\" limitGroup }"
	puts $fileid "  { \"On Job Complete\" onJobComplete e { $onJobCompletes } }"
	puts $fileid "  { \"Submit As Suspended\" submitSuspended b }"
	puts $fileid "  { \"Frame List\" frames }"
	puts $fileid "  { \"Task Chunk Size (1 or greater)\" chunkSize x}"
	puts $fileid "  { \"Render Threads (0 to use default)\" threadCount x}"
	puts $fileid "  { \"Max RAM Usage (0 to use default)\" ramUsage x}"
	puts $fileid "  { \"Build\" build e { $builds } }"
	puts $fileid "  { \"Submit Each Write Node As A Separate Job\" separateJobs b }"
	puts $fileid "  { \"Submit Nuke Scene File\" submitScript b }"
	puts $fileid "}"
	close $fileid
	
	# Source the submission dialog script, and return if there is an error
	# or if the user cancels the dialog.
	if {[ catch {
		source $deadlineTempTclFile
	} ]} {
		return
	}
	
	# Check priority value.
	if {![IsInteger $priority]} {
		message "Priority value $priority is not a valid integer"
		set priority 50
		set errors true
	}
	if { $priority < 0 || $priority > 100 } {
		message "Priority value must be between 0 and 100 inclusive"
		set priority 50
		set errors true
	}
	
	# Check machine limit value.
	if {![IsInteger $machineLimit]} {
		message "Machine Limit value $machineLimit is not a valid integer"
		set machineLimit 0
		set errors true
	}
	
	# Check task timeout value.
	if {![IsInteger $taskTimeout]} {
		message "Task Timeout value $taskTimeout is not a valid integer"
		set taskTimeout 0
		set errors true
	}
	
	# Check task chunk size value.
	if {![IsInteger $chunkSize]} {
		message "Task Chunk Size value $chunkSize is not a valid integer"
		set chunkSize 1
		set errors true
	}
	if { $chunkSize < 1 } {
		message "Task Chunk Size must be greater than or equal to 1"
		set chunkSize 1
		set errors true
	}
	
	# Check render threads value.
	if {![IsInteger $threadCount]} {
		message "Render Threads value $threadCount is not a valid integer"
		set threadCount 0
		set errors true
	}
	
	# Check ram usage value.
	if {![IsInteger $ramUsage]} {
		message "Max RAM Usage value $ramUsage is not a valid integer"
		set ramUsage 0
		set errors true
	}
}

# Write all the sticky settings to the config file.
catch {set fileid [open $deadlineConfigFile w]}
puts $fileid "$department"
puts $fileid "$group"
puts $fileid "$pool"
puts $fileid "$priority"
puts $fileid "$machineLimit"
puts $fileid "$chunkSize"
puts $fileid "$submitSuspended"
puts $fileid "$submitScript"
puts $fileid "$limitGroup"
puts $fileid "$separateJobs"
close $fileid

# Check file paths.
if {![CheckFilePaths $submitScript]} {
	return
}

# Check if we should be submitting a separate job for each write node.
set resultsString ""
foreach node $theNodes {
	# Check if we should enter the loop for this node.
	set enterLoop false
	if {!$separateJobs} {
		set enterLoop true
	} elseif {[class $node] == "Write" && [knob $node.disable] != true} {
		set enterLoop true
	}
	
	if {$enterLoop} {
		# Get correct chunk size and job name.
		set tempJobName $jobName
		set tempChunkSize $chunkSize
		if {$separateJobs} {
			set writeNodeName [knob $node.name]
			set tempChunkSize [GetChunkSizeForWriteNode $writeNodeName $chunkSize]
			set tempJobName [concat $jobName " - $writeNodeName"]
		}
		
		# Create the submission info file.
		catch {set fileid [open $submitInfoFile w]}
		puts $fileid "Plugin=Nuke"
		puts $fileid "Name=$tempJobName"
		puts $fileid "Comment=$comment"
		puts $fileid "Department=$department"
		puts $fileid "Group=$group"
		puts $fileid "Pool=$pool"
		puts $fileid "Priority=$priority"
		puts $fileid "MachineLimit=$machineLimit"
		puts $fileid "TaskTimeoutMinutes=$taskTimeout"
		puts $fileid "OnJobComplete=$onJobComplete"
		puts $fileid "Frames=$frames"
		puts $fileid "ChunkSize=$tempChunkSize"
		puts $fileid "LimitGroups=$limitGroup"
		
		# Check if the job should be submitted as suspended.
		if {$submitSuspended} {
			puts $fileid "InitialStatus=Suspended"
		}
		
		if {!$separateJobs} {
			# Add all the padded output filenames - and create the output directory.
			set index 0
			foreach tempNode $theNodes {
				if {[class $tempNode] == "Write" && [knob $tempNode.disable] != true } {
					file mkdir [file dirname [filename $tempNode]]
					set outputfile [GetPaddedFilename [filename $tempNode]]
					puts $fileid "OutputFilename$index=$outputfile"
					incr index
				}
			}
		} else {
			file mkdir [file dirname [filename $node]]
			set outputfile [GetPaddedFilename [filename $node]]
			puts $fileid "OutputFilename0=$outputfile"
		}
		
		close $fileid
		
		# Create the plugin info file.
		catch {set fileid [open $pluginInfoFile w]}
		puts $fileid "Version=$nuke_version_major"
		puts $fileid "Build=$build"
		puts $fileid "Threads=$threadCount"
		puts $fileid "RamUse=$ramUsage"
		if {$separateJobs} {
			set writeNodeName [knob $node.name]
			puts $fileid "WriteNode=$writeNodeName"
		}
		if {!$submitScript} {
			puts $fileid "SceneFile=[knob root.name]"
		}
		close $fileid
		
		# Submit the job to Deadline.
		catch {
			if {$submitScript} {
				if {[file exists "/Applications/Deadline/Resources/bin/deadlinecommandbg"] == 1} {
					exec "/Applications/Deadline/Resources/bin/deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $submitInfoFile $pluginInfoFile [knob root.name]
				} else {
					exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $submitInfoFile $pluginInfoFile [knob root.name]
				}
			} else {
				if {[file exists "/Applications/Deadline/Resources/bin/deadlinecommandbg"] == 1} {
					exec "/Applications/Deadline/Resources/bin/deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $submitInfoFile $pluginInfoFile
				} else {
					exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename $submitInfoFile $pluginInfoFile
				}
			}
		}
		
		# Append the results.
		catch {set fileid [open $outputFilename r]}
		set tempResultsString [read $fileid]
		close $fileid
		set resultsString [concat $resultsString "$tempResultsString\n\n"]
		
		# If we're only submitting one job, then break here.
		if {!$separateJobs} {
			break
		}
	}
}

# Show the results to the user.
message $resultsString
