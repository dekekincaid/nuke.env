# 
# dpxInfo v1.1 by Hakan Blomdahl
#
#  Usage: dpxInfo <mode> <symbol> [<symbol> ... ] <filename> 
#
#  Reads a header of DPX-file and returns the data in a readable form.
#  The returned data is formatted to be viewed with a fixed width font, like courier.
#  It is also very simple to parse (I quote values containing whitespaces.)
#  
#  <symbol> can be replaced with "all" to show ALL fields in the header. (for us lazy people).
#
#  Throws an error when there is problem.
#
#
#  To do:
#  * Decode more fields. (throw in the units for some fields. Like "bytes", "Hz", etc...)
#  * Include the missing 7 image elements. Although, no one uses them it seems... :-(
#
#
# Examples:
#
#   # Print all header info.
#   puts "[dpxInfo decode all img.0001.dpx]"
#
#
#   # Do your own fancy output:
#   foreach {symbol value} [dpxInfo decode all img.0001.dpx] {
#     puts " -- ${symbol} -- ${value} --"
#   }
#
#   # Print timecode:
#   puts "[dpxInfo singledecode tvTimeCode img.0001.dpx]"
#
#
#   # Get width and height
#   set data [dpxInfo singledecode iPixelsPerLine iLinesPerImage img.0001.dpx]
#   set width  [lindex ${data} 0]
#   set height [lindex ${data} 1]
#
#
#   # Get width and height (Tcl-array-style!)
#   array set header [dpxInfo decode all img.0001.dpx]
#   set width $header(iPixelsPerLine)
#   set height $header(iLinesPerImage)
#
#
# History:
# 1.0 first release.
# 1.1 Added Filmstock decoding.
#

proc dpxInfo { mode_ args } {

	# mode_

	switch -exact -- ${mode_} {

		
		singleraw {
			# Dont show symbols
			set _showSymbolNames 0
			set _decodeValues 0
		}
		singledecode {
			# Dont show symbols
			set _showSymbolNames 0
			set _decodeValues 1
		}

		raw {
			# The raw data
			set _showSymbolNames 1
			set _decodeValues 0
		}
		decode -
		default {
			# Decoded
			set _showSymbolNames 1
			set _decodeValues 1
		}
	}


	set textResult ""


	# The filename is the last parameter.
	set fileName [lindex ${args} end]

	# Rest is parameters and options.
	set symbols [lrange ${args} 0 end-1]
	
	
	if { [catch { open ${fileName} r } result] } {
		set errorMsg $result
		error "Error opening File: ${errorMsg}"
	}
	


	set fileHandle $result
	fconfigure ${fileHandle} -encoding binary
	
	set header [read ${fileHandle} 16384]
	# puts "Header read: [string length $header] bytes"
	catch { close $fileHandle }
	
	
	#	fMagic			@0I1


	binary scan ${header} @0a4 magic

	switch -exact -- ${magic} {
		"SDPX" {
			set _headerEntries {

				fMagic								@0a4
				fDataOffset							@4I1
				fVersion							@8A8
				fImageSize							@16I1
				fDittoKey							@20I1
				fGenericHeaderSize      			@24I1
				fIndustryHeaderSize     			@28I1
				fUserHeaderSize						@32I1
				fImageFilename						@36A100
				fCreationDate						@136A24
				fCreator							@160A100
				fProjectName						@260A200
				fCopyright							@460A200
				fEncryption							@660H8


				iOrientation						@768S1
				iElements							@770S1
				iPixelsPerLine						@772I1
				iLinesPerImage						@776I1

				ie1DataSign							@780I1
				ie1RefLowDataCode					@784I1
				ie1RefLowquantityRepresented		@788I1
				ie1RefHighDataCode					@792I1
				ie1RefHighquantityRepresented		@796I1
				ie1Descriptor						@800c1
				ie1TransferCharacteristic			@801c1
				ie1ColorimetricSpec					@802c1
				ie1BitSize							@803c1
				ie1Packing							@804S1
				ie1Encoding							@806S1
				ie1DataOffset						@808I1
				ie1EOLPadding						@812I1
				ie1EOIPadding						@816I1
				ie1Description						@820A32


				ioOffsetX							@1408I1
				ioOffsetY							@1412I1
				ioCenterX							@1416I1
				ioCenterY							@1420I1
				ioOriginalWidth						@1424I1
				ioOriginalHeight					@1428I1
				ioSourceFilename					@1432A100
				ioSourceDate						@1532A24
				ioInputDeviceName					@1556A32
				ioInputDeviceSerialNumber			@1588A32
				ioBorderXL							@1620S1
				ioBorderXR							@1622S1
				ioBorderYT							@1624S1
				ioBorderYB							@1626S1
				ioAspectHorizontal					@1628I1
				ioAspectVertical					@1632I1


				fManufacturer						@1664A2
				fFilmType							@1666A2
				fOffsetPerfs						@1668A2
				fPrefix								@1670A6
				fCount								@1676A4
				fFormat								@1680A32
				fFramePosInSequence					@1712I1
				fSequenceLength						@1716I1
				fHeldCount							@1720I1
				fFrameRateOriginal					@1724I1
				fShutterAngle						@1728I1
				fFrameID							@1732A32
				fSlateInfo							@1764A100

				tvSmpteTimeCode						@1920I1
				tvSmpteUserBits						@1924I1
				tvInterlace							@1928c1
				tvField								@1929c1
				tvVideoSignalStandard				@1930c1
				tvHorizontalSamplingRate			@1932I1
				tvVerticalSamplingRate				@1936I1
				tvTemporalSamplingRate				@1940I1
				tvTimeOffsetFromSyncToFirstPixel	@1940I1
				tvGamma								@1948I1
				tvBlackLevelCodeValue			   	@1952I1
				tvBlackGain  		   				@1956I1
				tvBreakPoint			   			@1960I1
				tvReferenceWhiteLevelCodeValue		@1964I1
				tvIntegrationTime					@1968I1

			}
		}
		"XPDS" {
			set _headerEntries {

				fMagic								@0a4
				fDataOffset							@4i1
				fVersion							@8A8
				fImageSize							@16i1
				fDittoKey							@20i1
				fGenericHeaderSize      			@24i1
				fIndustryHeaderSize     			@28i1
				fUserHeaderSize						@32i1
				fImageFilename						@36A100
				fCreationDate						@136A24
				fCreator							@160A100
				fProjectName						@260A200
				fCopyright							@460A200
				fEncryption							@660H8


				iOrientation						@768s1
				iElements							@770s1
				iPixelsPerLine						@772i1
				iLinesPerImage						@776i1

				ie1DataSign							@780i1
				ie1RefLowDataCode					@784i1
				ie1RefLowquantityRepresented		@788i1
				ie1RefHighDataCode					@792i1
				ie1RefHighquantityRepresented		@796i1
				ie1Descriptor						@800c1
				ie1TransferCharacteristic			@801c1
				ie1ColorimetricSpec					@802c1
				ie1BitSize							@803c1
				ie1Packing							@804s1
				ie1Encoding							@806s1
				ie1DataOffset						@808i1
				ie1EOLPadding						@812i1
				ie1EOIPadding						@816i1
				ie1Description						@820A32


				ioOffsetX							@1408i1
				ioOffsetY							@1412i1
				ioCenterX							@1416i1
				ioCenterY							@1420i1
				ioOriginalWidth						@1424i1
				ioOriginalHeight					@1428i1
				ioSourceFilename					@1432A100
				ioSourceDate						@1532A24
				ioInputDeviceName					@1556A32
				ioInputDeviceSerialNumber			@1588A32
				ioBorderXL							@1620s1
				ioBorderXR							@1622s1
				ioBorderYT							@1624s1
				ioBorderYB							@1626s1
				ioAspectHorizontal					@1628i1
				ioAspectVertical					@1632i1


				fManufacturer						@1664A2
				fFilmType							@1666A2
				fOffsetPerfs						@1668A2
				fPrefix								@1670A6
				fCount								@1676A4
				fFormat								@1680A32
				fFramePosInSequence					@1712i1
				fSequenceLength						@1716i1
				fHeldCount							@1720i1
				fFrameRateOriginal					@1724i1
				fShutterAngle						@1728i1
				fFrameID							@1732A32
				fSlateInfo							@1764A100

				tvSmpteTimeCode						@1920i1
				tvSmpteUserBits						@1924i1
				tvInterlace							@1928c1
				tvField								@1929c1
				tvVideoSignalStandard				@1930c1
				tvHorizontalSamplingRate			@1932i1
				tvVerticalSamplingRate				@1936i1
				tvTemporalSamplingRate				@1940i1
				tvTimeOffsetFromSyncToFirstPixel	@1940i1
				tvGamma								@1948i1
				tvBlackLevelCodeValue			   	@1952i1
				tvBlackGain  		   				@1956i1
				tvBreakPoint			   			@1960i1
				tvReferenceWhiteLevelCodeValue		@1964i1
				tvIntegrationTime					@1968i1

			}
		}
		default {
			error "Not a DPX file: \"${fileName}\""
		}
	}

	
	array set _head $_headerEntries
	
	
	
	if { ${symbols} eq "all" } {
		set symbols {}
		foreach { symbol ignore } $_headerEntries {
			lappend symbols ${symbol}
		}
	}


	
	set symbolList {}
	set patternString ""
	



	# Build up a symbol-list and variable destinations for the binary scan command:
	foreach symbol ${symbols} {
		if { ![info exists _head(${symbol})] } {
			error "\"${symbol}\" is not a valid symbol."
		}
		set _result(${symbol}) 0
	
		lappend symbolList "_result(${symbol})"
		append patternString $_head(${symbol})
	}


	# Alright. EXECUTE the binary scan.
	if { [llength symbolList] > 0 } {
		eval binary scan [list ${header}] [list ${patternString}] ${symbolList}
	}



	#
	#
	# Done with reading the header. Do post-process of the values.
	#
	#

	# IEE conversion. With the help from this lovely procedure from the tcl-wikipedia:
	# This does not handle 0 properly, but since I have no Idea what it is doing, I wont do any 0-fixes here.
	proc IEEE2float {data byteorder} {
		if {$byteorder == 0} {
			set code [binary scan $data cccc se1 e2f1 f2 f3]
		} else {
			set code [binary scan $data cccc f3 f2 e2f1 se1]
		}
		
		set se1  [expr {($se1 + 0x100) % 0x100}]
		set e2f1 [expr {($e2f1 + 0x100) % 0x100}]
		set f2   [expr {($f2 + 0x100) % 0x100}]
		set f3   [expr {($f3 + 0x100) % 0x100}]
		
		set sign [expr {$se1 >> 7}]
		set exponent [expr {(($se1 & 0x7f) << 1 | ($e2f1 >> 7))}]
		set f1 [expr {$e2f1 & 0x7f}]
		
		set fraction [expr {double($f1)*0.0078125 + \
				double($f2)*3.0517578125e-05 + \
				double($f3)*1.19209289550781e-07}]
		
		set res [expr {($sign ? -1. : 1.) * \
				pow(2.,double($exponent-127)) * \
				(1. + $fraction)}]
		return $res
	}

	# Convert IEEE to native float and deal with them. Tricky with 64bit systems. Phew!
	
	# The floats!
	foreach symbol {

		ie1RefLowquantityRepresented
		ie1RefHighquantityRepresented

		ioCenterX
		ioCenterY

		fFrameRateOriginal
		fShutterAngle

		tvHorizontalSamplingRate
		tvVerticalSamplingRate
		tvTemporalSamplingRate
		tvTimeOffsetFromSyncToFirstPixel
		tvGamma
		tvBlackLevelCodeValue
		tvBlackGain
		tvBreakPoint
		tvReferenceWhiteLevelCodeValue
		tvIntegrationTime
	} {

		if { [info exists _result(${symbol})] } {

			# The data is expanded to doubles on some systems. Mask!
			set _result(${symbol}) [expr { $_result(${symbol}) & 0xFFFFFFFF }]

			if { $_result(${symbol}) == 0xffffffff } {
				catch { unset  _result(${symbol}) }
			} else {
				
				if { $_result(${symbol}) == 0 } {
					set _result(${symbol}) 0.0
				} else {
					set _result(${symbol}) [IEEE2float [binary format {I1} $_result(${symbol})] 0]
				}
			}
		}
	}

	# The unsigned 32bit values!
	foreach symbol {

		fImageSize
		fDittoKey
		fGenericHeaderSize
		fIndustryHeaderSize
		fUserHeaderSize

		iPixelsPerLine
		iLinesPerImage

		ie1RefLowDataCode
		ie1RefHighDataCode

		ioOffsetX
		ioOffsetY
		ioOriginalWidth
		ioOriginalHeight
		ioAspectHorizontal
		ioAspectVertical

		fFramePosInSequence
		fSequenceLength
		fHeldCount

   		tvSmpteTimeCode
		tvSmpteUserBits


	} {
		if { [info exists _result(${symbol})] } {

			# Just in case the integer data is expanded to 64bit on some systems. Mask!
			set _result(${symbol}) [expr { $_result(${symbol}) & 0xFFFFFFFF }]

			if { $_result(${symbol}) == 0xffffffff } {
				catch { unset  _result(${symbol}) }
			}
		}
	}


	# The 16bit values!
	foreach symbol {

		iOrientation
		iElements

		ie1Packing
		ie1Encoding

		ioBorderXL
		ioBorderXR
		ioBorderYT
		ioBorderYB
	} {
		if { [info exists _result(${symbol})] } {

			# Mask!
			set _result(${symbol}) [expr { $_result(${symbol}) & 0xFFFF }]

			if { $_result(${symbol}) == 0xffff } {
				catch { unset  _result(${symbol}) }
			}
		}
	}


	# The 8bit values!
	foreach symbol {

		ie1Descriptor
		ie1TransferCharacteristic
		ie1ColorimetricSpec
		ie1BitSize

		tvInterlace
		tvField
		tvVideoSignalStandard

	} {
		if { [info exists _result(${symbol})] } {

			# Mask!
			set _result(${symbol}) [expr { $_result(${symbol}) & 0xFFFF }]

			if { $_result(${symbol}) == 0xffff } {
				catch { unset  _result(${symbol}) }
			}
		}
	}


	if { ${_decodeValues} } {


		if { [info exists _result(fManufacturer)] && [info exists _result(fFilmType)] } {


			switch -exact -- $_result(fManufacturer) {
				01 -
				11 {
	
					set decodeTable {
						Agfa	A	20	N	"XT 100"
						Agfa	A	24	M	"XTR 250"
						Agfa	A	83	F	"XT 320"
						Agfa	A	84	S	"XTS 400"
					}
					set decodedManufacturerChar	"A"
					set decodedManufacturer		"Agfa"
				}
				02 -
				12 -
				22 {
					# Depending on filmstock-code, it can be either Kodak or Eastman.
					# Phew...

					set decodeTable {
						Kodak	K	00	P "5600 (obsolete)"
						Kodak	K	14	X "SO-214 SFX 200T"
						Kodak	K	20	Y "5620 Prime Time (obsolete)"
						Kodak	K	22	E "5222/7222"
						Kodak	K	24	L "5224 (obsolete)"
						Kodak	K	31	H "5231/7231"
						Kodak	K	34	D "5234/7234"
						Kodak	K	43	A "5243/7243 (obsolete)"
						Kodak	K	44	V "5244/7244 (obsolete)"
						Kodak	K	45	K "5245/7245"
						Kodak	K	46	I "5246/7246 Vision 250D"
						Kodak	K	47	B "5247/7247 (obsolete)"
						Kodak	K	48	M "5248/7248"
						Kodak	K	49	O "5649 (obsolete)"
						Kodak	K	72	S "5272/7272"
						Kodak	K	74	Z "5274/7274 Vision 200T"
						Kodak	K	77	Q "5277/7277"
						Kodak	K	79	U "5279/7279"
						Kodak	K	87	W "5287/7287 (obsolete)"
						Kodak	K	89	R "5289 Vision 800T"
						Kodak	K	92	N "7292 (obsolete)"
						Kodak	K	93	L "5293/7293"
						Kodak	K	94	G "5294/7294 (obsolete)"
						Kodak	K	95	F "5295 (obsolete)"
						Kodak	K	96	J "5296/7296 (obsolete)"
						Kodak	K	97	C "5297/7297 (obsolete)"
						Kodak	K	98	T "5298/7298 (obsolete)"

						Eastman	E	01	K "5201/7201 Vision2 50D"
						Eastman	E	05	Q "5205/7205 Vision2 250D"
						Eastman	E	12	M "5212/7212 Vision2 100T"
						Eastman	E	17	L "5217/7217 Vision2 200T"
						Eastman	E	18	H "5218/7218 Vision2 500T"
						Eastman	E	29	B "5229/7229 Vision2 Expression 500T"
						Eastman	E	42	V "5242/7242 Vision Intermediate"
						Eastman	E	63	E "5263/7263 Vision 500T"
						Eastman	E	65	C "7265"
						Eastman	E	66	D "7266"
						Eastman	E	84	G "5284/7284 Vision Expresssion 500T"
						Eastman	E	85	A "5285 100D"
						Eastman	E	99	I "7299"
					}
					# Remember, these will be overriden if a stock is found:
					set decodedManufacturerChar	"?"
					set decodedManufacturer		"Kodak or Eastman"

				}
				03 -
				13 -
				23 {

					set decodeTable {
						Fuji	F	01	I	"F-CI (8501, 8601, 8701) (obsolete 95)"
						Fuji	F	02	I	"F-CI (8502, 8602, 8702)"
						Fuji	F	10	N	"F-64 (obsolete 05/95)"
						Fuji	F	13	I	"F-CI (obsolete)"
						Fuji	F	14	N	"F-500 (obsolete)"
						Fuji	F	20	N	"F-64D (obsolete 05/95)"
						Fuji	F	21	N	"F-64D (8521, 8621, 8721) (obsolete 98)"
						Fuji	F	22	N	"F-64D (8522, 8622)"
						Fuji	F	30	N	"F-125 (obsolete 05/95)"
						Fuji	F	31	N	"F-125 (8531, 8631, 8731) (obsolete 98)"
						Fuji	F	32	N	"F-125 (8532, 8632)"
						Fuji	F	40	R	"VELVIA color reversal (8540)"
						Fuji	F	50	N	"F-250 (obsolete 05/95)"
						Fuji	F	51	N	"F-250 (8551, 8651, 8751) (obsolete 99)"
						Fuji	F	52	N	"F-250 (8552, 8652)"
						Fuji	F	53	N	"ETERNA 250 (8553, 8653)"
						Fuji	F	60	N	"F-250D (obsolete 05/95)"
						Fuji	F	61	N	"F-250D (8561, 8661, 8761) (obsolete 99)"
						Fuji	F	62	N	"F-250D (8562, 8662)"
						Fuji	F	63	N	"ETERNA 250D (8563, 8663)"
						Fuji	F	70	N	"F-500 (8570, 8670, 8770) (obsolete 95)"
						Fuji	F	71	N	"F-500 (8571, 8671) (obsolete 99)"
						Fuji	F	72	N	"F-500 (8572, 8672)"
						Fuji	F	73	N	"ETERNA 500 (8573, 8673)"
						Fuji	F	82	N	"F-400 (8582, 8682)"
						Fuji	F	83	N	"ETERNA 400 (8592, 8692)"
						Fuji	F	92	N	"REALA 500D (8592, 8692)"
					}
					set decodedManufacturerChar	"F"
					set decodedManufacturer		"Fuji"
				}
			}

			if { [info exists decodeTable] } {
				foreach { manufacturer manufacturerChar emulsioncode emulsionChar filmtype } ${decodeTable} {

					if { [string equal $_result(fFilmType) ${emulsioncode}] } {
						set decodedManufacturerChar	${manufacturerChar}
						set decodedManufacturer		${manufacturer}
						set decodedEmulsionChar		${emulsionChar}
						set decodedFilmtype			${filmtype}
						break
					}
				}
			}

			if { [info exists decodedManufacturer] } {
				set _result(fManufacturer) "$_result(fManufacturer) ${decodedManufacturerChar} ${decodedManufacturer}"
			}

			if { [info exists decodedFilmtype] } {
				set _result(fFilmType) "$_result(fFilmType) ${decodedEmulsionChar} ${decodedFilmtype}"
			}
		}

		if { [info exists _result(tvSmpteTimeCode)] } {

			set val  $_result(tvSmpteTimeCode) 

			# Convert SMPTE timecode (read in as an 32 bit integer) to something readable.

			set hh	[format "%0x" [expr { ( $val >> 24 ) & 0xFF }]]
			set mm	[format "%0x" [expr { ( $val >> 16 ) & 0xFF }]]
			set ss	[format "%0x" [expr { ( $val >>  8 ) & 0xFF }]]
			set ff	[format "%0x" [expr { $val & 0xFF }]]

			set tc [format "%02d:%02d:%02d:%02d" ${hh} ${mm} ${ss} ${ff}]

			set _result(tvSmpteTimeCode) "${tc}"

		}

		if { [info exists _result(tvInterlace)] } {
			switch -exact -- $_result(tvInterlace) {
				0 {
					set decoded "Non Interlaced"
				}
				1 {
					set decoded "2:1 Interlaced"
				}
				default {
					set decoded "?"
				}
			}
			set  _result(tvInterlace) "${decoded}"
		}

		if { [info exists _result(tvVideoSignalStandard)] } {
			switch -exact -- $_result(tvVideoSignalStandard) {
				0 {
					set decoded "undefined"
				}
				1 {
					set decoded "NTSC"
				}
				2 {
					set decoded "PAL"
				}
				3 {
					set decoded "PAL-M"
				}
				4 {
					set decoded "SECAM"
				}
				50 {
					set decoded "YCBCR CCIR 601-2 525-line, 2:1 interlace, 4:3 aspect ratio"
				}
				51 {
					set decoded "YCBCR CCIR 601-2 625-line, 2:1 interlace, 4:3 aspect ratio"
				}
				100 {
					set decoded "YCBCR CCIR 601-2 525-line, 2:1 interlace, 16:9 aspect ratio"
				}
				101 {
					set decoded "YCBCR CCIR 601-2 625-line, 2:1 interlace, 16:9 aspect ratio"
				}
				150 {
					set decoded "YCBCR 1050-line, 2:1 interlace, 16:9 aspect ratio"
				}
				151 {
					set decoded "YCBCR 1125-line, 2:1 interlace, 16:9 aspect ratio (SMPTE 240M)"
				}
				152 {
					set decoded "YCBCR 1250-line, 2:1 interlace, 16:9 aspect ratio"
				}
				200 {
					set decoded "YCBCR 525-line, 1:1 progressive, 16:9 aspect ratio"
				}
				201 {
					set decoded "YCBCR 625-line, 1:1 progressive, 16:9 aspect ratio"
				}
				202 {
					set decoded "YCBCR 787.5-line, 1:1 progressive, 16:9 aspect ratio"
				}
				default {
					if { ( $_result(tvVideoSignalStandard) >= 5 ) && ( $_result(tvVideoSignalStandard) <= 49 ) } {
						set elemString "Value ($_result(tvVideoSignalStandard)) reserved for composite video"
					}
					if { ( $_result(tvVideoSignalStandard) >= 52 ) && ( $_result(tvVideoSignalStandard) <= 99 ) } {
						set elemString "Value ($_result(tvVideoSignalStandard)) reserved for component video"
					}
					if { ( $_result(tvVideoSignalStandard) >= 102 ) && ( $_result(tvVideoSignalStandard) <= 149 ) } {
						set elemString "Value ($_result(tvVideoSignalStandard)) reserved for future widescreen"
					}
					if { ( $_result(tvVideoSignalStandard) >= 153 ) && ( $_result(tvVideoSignalStandard) <= 199 ) } {
						set elemString "Value ($_result(tvVideoSignalStandard)) reserved for future high-definition interlace"
					}
					if { ( $_result(tvVideoSignalStandard) >= 203 ) && ( $_result(tvVideoSignalStandard) <= 254 ) } {
						set elemString "Value ($_result(tvVideoSignalStandard)) reserved for future high-definition progressive"
					}
				}
			}
			set  _result(tvVideoSignalStandard) "${decoded}"
		}




		# Color transfer
		if { [info exists _result(ie1TransferCharacteristic)] } {
			switch -exact -- $_result(ie1TransferCharacteristic) {
				0 {
					set decoded "User Defined"
				}
				1 {
					set decoded "Printing Density"
				}
				2 {
					set decoded "Linear"
				}
				3 {
					set decoded "Logaritmic"
				}
				4 {
					set decoded "Unspecified Video"
				}
				5 {
					set decoded "SMPTE 240M"
				}
				6 {
					set decoded "CCIR 709-1"
				}
				7 {
					set decoded "CCIR 601-2 System B or G (625)"
				}
				8 {
					set decoded "CCIR 601-2 System M (525)"
				}
				9 {
					set decoded "Composite video (NTSC); see SMPTE 170M"
				}
				10 {
					set decoded "Composite video (PAL); see CCIR 624-4"
				}
				11 {
					set decoded "Z (depth) -- linear"
				}
				12 {
					set decoded "Z (depth) -- homogeneous (distance to screen and angle of view must also be specified in usr defined section)"
				}
				default {
					set decoded "Value ($_result(ie1TransferCharacteristic)) reserved for future use"
				}
			}
			set  _result(ie1TransferCharacteristic) "${decoded}"
		}


		# Color transfer
		if { [info exists _result(ie1ColorimetricSpec)] } {
			switch -exact -- $_result(ie1ColorimetricSpec) {
				0 {
					set decoded "User Defined"
				}
				1 {
					set decoded "Printing Density"
				}
				2 {
					set decoded "Not Applicable"
				}
				3 {
					set decoded "Not Applicable"
				}
				4 {
					set decoded "Unspecified Video"
				}
				5 {
					set decoded "SMPTE 240M"
				}
				6 {
					set decoded "CCIR 709-1"
				}
				7 {
					set decoded "CCIR 601-2 System B or G (625)"
				}
				8 {
					set decoded "CCIR 601-2 System M (525)"
				}
				9 {
					set decoded "Composite video (NTSC); see SMPTE 170M"
				}
				10 {
					set decoded "Composite video (PAL); see CCIR 624-4"
				}
				11 {
					set decoded "Not Applicable"
				}
				12 {
					set decoded "Not Applicable"
				}
				default {
					set decoded "Value ($_result(ie1ColorimetricSpec)) resereved for future use"
				}
			}
			set  _result(ie1ColorimetricSpec) "${decoded}"
		}


		if { [info exists _result(iOrientation)] } {
			switch -exact -- $_result(iOrientation) {
				0 {
					set orientString "Left to Right, Top to Bottom"
				}
				1 {
					set orientString "Right to Left, Top to Bottom"
				}
				2 {
					set orientString "Left to Right, Bottom to Top"
				}
				3 {
					set orientString "Right to Left, Top to Bottom"
				}
				4 {
					set orientString "Top to Bottom, Left to Right"
				}
				5 {
					set orientString "Top to Bottom, Right to Left"
				}
				6 {
					set orientString "Bottom to Top, Left to Right"
				}
				7 {
					set orientString "Top to Bottom, Right to Left"
				}
				default {
					set orientString "Unknown"
				}
			}
			set  _result(iOrientation) "${orientString}"

		}


		if { [info exists _result(ie1Descriptor)] } {
			switch -exact -- $_result(ie1Descriptor) {
				0 {
					set elemString "User defined (or unspecified single component)"
				}
				1 {
					set elemString "Red (R)"
				}
				2 {
					set elemString "Green (G)"
				}
				3 {
					set elemString "Blue (B)"
				}
				4 {
					set elemString "Alpha(matte)"
				}
				6 {
					set elemString "Luminance (Y)"
				}
				7 {
					set elemString "Chrominance (CB, CR, subsampled by two)"
				}
				8 {
					set elemString "Depth (Z)"
				}
				9 {
					set elemString "Composite video"
				}
				50 {
					set elemString "R,G,B"
				}
				51 {
					set elemString "R,G,B, alpha"
				}
				52 {
					set elemString "Alpha, B, G, R"
				}
				100 {
					set elemString "CB, Y, CR, Y (4:2:2) ---- based on SMPTE 125M"
				}
				101 {
					set elemString "CB, Y, a, CR, Y, a (4:2:2:4)"
				}
				102 {
					set elemString "CB, Y, CR (4:4:4)"
				}
				103 {
					set elemString "CB, Y, CR, a (4:4:4:4)"
				}
				150 {
					set elemString "User-defined 2-component element"
				}
				151 {
					set elemString "User-defined 3-component element"
				}
				152 {
					set elemString "User-defined 4-component element"
				}
				153 {
					set elemString "User-defined 5-component element"
				}
				154 {
					set elemString "User-defined 6-component element"
				}
				155 {
					set elemString "User-defined 7-component element"
				}
				156 {
					set elemString "User-defined 8-component element"
				}
				default {
					if { ( $ieImageDescriptor >= 157 ) && ( $ieImageDescriptor <= 254 ) } {
						set elemString "Reserved for future formats"
					}
					if { ( $ieImageDescriptor >= 10 ) && ( $ieImageDescriptor <= 49 ) } {
						set elemString "Reserved for future single components"
					}
					if { ( $ieImageDescriptor >= 53 ) && ( $ieImageDescriptor <= 99 ) } {
						set elemString "Reserved for future RGB ++ formats"
					}
					if { ( $ieImageDescriptor >= 104 ) && ( $ieImageDescriptor <= 149 ) } {
						set elemString "Reserved for future CBYCR ++ formats"
					}
				}
			}
			set  _result(ie1Descriptor) "${elemString}"
		}
	}










	#
	# Prepare the output.
	#
	if { ${_showSymbolNames} } {
	

		# Calculate the padding for some nice formatting.
		set pad 0
		foreach symbol ${symbols} {
			if { [string length ${symbol}] > ${pad} } {
				set pad [string length ${symbol}]
			}
		}


		foreach symbol ${symbols} {

			set sym [format "%${pad}s" ${symbol}]

			if { ![info exists _result(${symbol})] } {
				append textResult "${sym} undefined\n"
				continue
			}

			set v $_result(${symbol})
			set replaceCount [regsub -all -- {[^[:graph:] /t]+} $v {} w]
			if { ${replaceCount} > 0 } {
				# puts "Warning: unprintable characters"
				set v ${w}
			}
			# Quote if neccesary. Keeping strict pairs for simplified parsing
			if { ( [llength ${v}] > 1 ) || ( [string length ${v}] < 1 ) } {
				set v "\"${v}\""
			}
	
			append textResult "${sym} ${v}\n"
	
		}


	} else {


		foreach symbol ${symbols} {
			if { ![info exists _result(${symbol})] } {
				append textResult "undefined\n"
				continue
			}
			set v $_result(${symbol})
			set replaceCount [regsub -all -- {[^[:graph:] /t]+} $v {} w]
			if { ${replaceCount} > 0 } {
				# puts "Warning: unprintable characters"
				set v ${w}
			}
			# Quote if neccesary. Keeping strict pairs for simplified parsing
			if { ( [llength ${v}] > 1 ) || ( [string length ${v}] < 1 ) } {
				set v "\"${v}\""
			}
	
			append textResult "${v}\n"
		}
		append textResult "\n"
	}
	
	return ${textResult}
}
