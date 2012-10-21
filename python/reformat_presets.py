# reformat_presets.py
#
# Author: 
# Deke Kincaid
# The Foundry
# dekekincaid@gmail.com
#
# v1.0
# 8/12/11
#
# user presets for the reformat node.  The most common file formats out there so you don't have to remember them anymore
#
# only works with Nuke 6.3v1 and above
# Install Instructions:
# 1. copy the file into your .nuke folder or anywhere in your NUKE_PATH 
# 2. in your init.py or menu.py put the following code:
# import reformat_presets
# reformat_presets.nodePresetReformat()
#
# Any issues or additional formats you would like added to this tool then email me or post a reply in the comments on nukepedia
# dekekincaid@gmail.com
import nuke
def nodePresetReformat():
	  nuke.setPreset("Reformat", "540p", {'box_height': '540', 'box_width': '960', 'type': 'to box', 'box_fixed': 'true', 'label': '1080p half\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "720p", {'box_height': '720', 'box_width': '1280', 'type': 'to box', 'box_fixed': 'true', 'label': '720p\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "1080p", {'box_height': '1080', 'box_width': '1920', 'type': 'to box', 'box_fixed': 'true', 'label': '1080p\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SI2k", {'box_height': '1152', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'SI2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "HDCAM", {'box_height': '1080', 'box_width': '1440', 'type': 'to box', 'box_fixed': 'true', 'box_pixel_aspect': '1.5', 'label': 'HDCAM\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Super35", {'box_height': '1556', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'Super35\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "Arri/Alexa Raw 16:9", {'box_height': '1620', 'box_width': '2880', 'type': 'to box', 'box_fixed': 'true', 'label': 'Arri Alexa Raw 16:9\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Arri/D21 Raw 1.33", {'box_height': '2160', 'box_width': '2880', 'type': 'to box', 'box_fixed': 'true', 'label': 'Arri D21 Raw 1.33\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Arri/D21 Raw 16:9", {'box_height': '1620', 'box_width': '2880', 'type': 'to box', 'box_fixed': 'true', 'label': 'Arri D21 Raw 16:9\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "DCP/HDTV 1920x1080 16:9", {'box_height': '1080', 'box_width': '1920', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP HDTV\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/Flat 1998x1080 1.85", {'box_height': '1080', 'box_width': '1998', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP Flat\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/Scope 2048x858 2.39", {'box_height': '858', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP Scope\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/Full 2048x1080 1.896", {'box_height': '1080', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP Full\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/---------------", {})
	  nuke.setPreset("Reformat", "DCP/HDTV 3840x2160 16:9", {'box_height': '2160', 'box_width': '3840', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP HDTV 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/Flat 3996x2160 1.85", {'box_height': '2160', 'box_width': '3996', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP Flat 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/Scope 4096x1716 2.39", {'box_height': '1716', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP Scope 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DCP/Full 4096x2160 1.896", {'box_height': '2160', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'DCP Full 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "DVCPro/HD 720p", {'box_fixed': 'true', 'box_height': '720', 'box_width': '960', 'type': 'to box', 'box_pixel_aspect': '1.33', 'label': 'DVCProHD 720p\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DVCPro/HD 1080i50", {'box_fixed': 'true', 'box_height': '1080', 'box_width': '1440', 'type': 'to box', 'box_pixel_aspect': '1.33', 'label': 'DVCProHD 1080i50\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "DVCPro/HD 1080i60", {'box_fixed': 'true', 'box_height': '1080', 'box_width': '1280', 'type': 'to box', 'box_pixel_aspect': '1.5', 'label': 'DVCProHD 1080i60\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "Film 1k/Full 1.316", {'box_height': '778', 'box_width': '1024', 'type': 'to box', 'box_fixed': 'true', 'label': 'Full Aperture 1k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 1k/Super 1.85", {'box_height': '554', 'box_width': '1024', 'type': 'to box', 'box_fixed': 'true', 'label': 'Super 1.85 1k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 1k/S35 Techniscope 2.40", {'box_height': '466', 'box_width': '1024', 'type': 'to box', 'box_fixed': 'true', 'label': 'S35 Techniscope 1k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 1k/Academy 1.37", {'box_height': '666', 'box_width': '914', 'type': 'to box', 'box_fixed': 'true', 'box_fixed': 'true', 'label': 'Academy 1k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 1k/Cinemascope 2.35", {'box_height': '778', 'box_width': '914', 'type': 'to box', 'box_fixed': 'true', 'box_pixel_aspect': '2.00', 'label': 'Cinemascope 1k\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 1k/Vistavision 1.5", {'box_height': '1024', 'box_width': '1548', 'type': 'to box', 'box_fixed': 'true', 'box_fixed': 'true', 'label': 'Vistavision 1k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 1k/70mm 2.2", {'box_height': '460', 'box_width': '1024', 'type': 'to box', 'box_fixed': 'true', 'label': '70mm 1k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "Film 2k/Full 1.316", {'box_height': '1556', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'Full Aperture 2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 2k/Super 1.85", {'box_height': '1108', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'Super 1.85 2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 2k/S35 Techniscope 2.40", {'box_height': '932', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'S35 Techniscope 2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 2k/Academy 1.37", {'box_height': '1332', 'box_width': '1828', 'type': 'to box', 'box_fixed': 'true', 'box_fixed': 'true', 'label': 'Academy 2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 2k/Cinemascope 2.35", {'box_height': '1556', 'box_width': '1828', 'type': 'to box', 'box_fixed': 'true', 'box_pixel_aspect': '2.00', 'label': 'Cinemascope 2k\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 2k/Vistavision 1.5", {'box_height': '2048', 'box_width': '3096', 'type': 'to box', 'box_fixed': 'true', 'box_fixed': 'true', 'label': 'Vistavision 2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 2k/70mm 2.2", {'box_height': '920', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': '70mm 2k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "Film 4k/Full 1.316", {'box_height': '3112', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'Full Aperture 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 4k/Super 1.85", {'box_height': '2216', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'Super 1.85 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 4k/S35 Techniscope 2.40", {'box_height': '1708', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'S35 Techniscope 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 4k/Academy 1.37", {'box_height': '2664', 'box_width': '3656', 'type': 'to box', 'box_fixed': 'true', 'box_fixed': 'true', 'label': 'Academy 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 4k/Cinemascope 2.35", {'box_height': '3112', 'box_width': '3656', 'type': 'to box', 'box_fixed': 'true', 'box_pixel_aspect': '2.00', 'label': 'Cinemascope 2k\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 4k/Vistavision 1.5", {'box_height': '4096', 'box_width': '6144', 'type': 'to box', 'box_fixed': 'true', 'box_fixed': 'true', 'label': 'S35 Techniscope 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Film 4k/70mm 2.2", {'box_height': '1840', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': '70mm 4k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "Imax Digital 1.37", {'box_height': '4096', 'box_width': '5616', 'type': 'to box', 'box_fixed': 'true', 'label': 'Imax Digital\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "Red/RedOne 2k 16:9", {'box_height': '1152', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 2k 16:9\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 2k 2:1", {'box_height': '1024', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 2k 2:1\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 2k ANA", {'box_height': '1152', 'box_width': '1408', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 2k ANA\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/---------------", {})
	  nuke.setPreset("Reformat", "Red/RedOne 3k 16:9", {'box_height': '1728', 'box_width': '3072', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 3k 16:9\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 3k 2:1", {'box_height': '1536', 'box_width': '3072', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 3k 2:1\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 3k ANA", {'box_height': '1728', 'box_width': '2112', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 3k ANA\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/----------------", {})
	  nuke.setPreset("Reformat", "Red/RedOne 4k 16:9", {'box_height': '2304', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 4k 16:9\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 4k 2:1", {'box_height': '2048', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 4k 2:1\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 4k HD", {'box_height': '2160', 'box_width': '3840', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 4k HD\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 4k ANA", {'box_height': '2304', 'box_width': '2816', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 4k ANA\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/RedOne 4.5k WS", {'box_height': '1920', 'box_width': '4480', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red One 4.5k WS\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/--------", {})
	  nuke.setPreset("Reformat", "Red/Epic 5k", {'box_height': '2700', 'box_width': '5120', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red Epic 5k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/Epic 6k", {'box_height': '4000', 'box_width': '6000', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red Epic 6k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/Epic 9k", {'box_height': '7000', 'box_width': '9334', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red Epic 9k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Red/Epic 28k", {'box_height': '9334', 'box_width': '28000', 'type': 'to box', 'box_fixed': 'true', 'label': 'Red Epic 28k\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Texture/1k Square", {'box_height': '1024', 'box_width': '1024', 'type': 'to box', 'box_fixed': 'true', 'label': '1k Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Texture/2k Square", {'box_height': '2048', 'box_width': '2048', 'type': 'to box', 'box_fixed': 'true', 'label': '2k Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Texture/4k Square", {'box_height': '4096', 'box_width': '4096', 'type': 'to box', 'box_fixed': 'true', 'label': '4k Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Texture/8k Square", {'box_height': '8192', 'box_width': '8192', 'type': 'to box', 'box_fixed': 'true', 'label': '8k Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Texture/16k Square", {'box_height': '16384', 'box_width': '16384', 'type': 'to box', 'box_fixed': 'true', 'label': '16k Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "Texture/32k Square", {'box_height': '32768', 'box_width': '32768', 'type': 'to box', 'box_fixed': 'true', 'label': '32k Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "SD/NTSC D1", {'box_fixed': 'true', 'box_height': '486', 'box_width': '720', 'type': 'to box', 'box_pixel_aspect': '0.91', 'label': 'NTSC\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/NTSC DV", {'box_fixed': 'true', 'box_height': '480', 'box_width': '720', 'type': 'to box', 'box_pixel_aspect': '0.91', 'label': 'NTSC DV\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/NTSC 16:9", {'box_fixed': 'true', 'box_height': '486', 'box_width': '720', 'type': 'to box', 'box_pixel_aspect': '1.21', 'label': 'NTSC 16:9\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/NTSC Square", {'box_height': '540', 'box_width': '720', 'type': 'to box', 'box_fixed': 'true', 'label': 'NTSC Square\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/---------------", {})
	  nuke.setPreset("Reformat", "SD/PAL D1", {'box_fixed': 'true', 'box_height': '576', 'box_width': '720', 'type': 'to box', 'box_pixel_aspect': '1.066', 'label': 'PAL D1\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/PAL DV", {'box_fixed': 'true', 'box_height': '576', 'box_width': '720', 'type': 'to box', 'box_pixel_aspect': '1.091', 'label': 'PAL DV\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/PAL 16:9", {'box_fixed': 'true', 'box_height': '576', 'box_width': '720', 'type': 'to box', 'box_pixel_aspect': '1.46', 'label': 'PAL 16:9\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "SD/480p", {'box_height': '480', 'box_width': '852', 'type': 'to box', 'box_fixed': 'true', 'box_pixel_aspect': '1.5', 'label': '480p\n([value box_width]x[value box_height] [value box_pixel_aspect])', 'note_font': 'Helvetica'})

	  nuke.setPreset("Reformat", "UHDTV/WQHD 16:9", {'box_height': '1440', 'box_width': '2560', 'type': 'to box', 'box_fixed': 'true', 'label': 'UHDTV WQHD\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "UHDTV/QFHD 16:9", {'box_height': '2160', 'box_width': '3840', 'type': 'to box', 'box_fixed': 'true', 'label': 'UHDTV QFHD\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})
	  nuke.setPreset("Reformat", "UHDTV/4320p 16:9", {'box_height': '4320', 'box_width': '7680', 'type': 'to box', 'box_fixed': 'true', 'label': 'UHDTV 4320p\n([value box_width]x[value box_height])', 'note_font': 'Helvetica'})

