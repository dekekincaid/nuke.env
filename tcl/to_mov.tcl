# to_mov
# mov@cgpolis.com

set movwriterdir [file dirname [plugin_name]]/to_mov
proc to_mov {} {
global movwriterdir
foreach n [nodes] {knob $n.selected false}
StickyNote {
 name to_Mov
 tile_color 0x3e3d3a00
 gl_color 0xff000000
 label "@b Mov writer@n\n @s-3 v0.1f"
 note_font_color 0xbd330000
 selected false
 addUserKnob {20 "" l to_mov}
 addUserKnob {1 plugdir l INVISIBLE}
 addUserKnob {32 knob l "@b@s+8@C0xff000000 Execute " T "set movwriterdir \[knob plugdir]\n\$movwriterdir/mov_writer"} 
#addUserKnob {32 knob l "@b@s+8@C0xff000000 Execute " T $movwriterdir/mov_writer}
 addUserKnob {6 pal l text t "check this to write .mov file with text overlay "}
 pal true
 addUserKnob {6 clean t "check this to write .mov file without text overlay "}
 clean true
 addUserKnob {6 range l "auto framerange" t "check this to use framerange of the read node or root.framerange if write node selected"}
 range true
 addUserKnob {6 log l "mov log" t "writes a txt file with time of creation and the paths of source sequence and the final mov files"}
 addUserKnob {20 texts l "text settings" t "text settings" n 1}
 texts 0
 addUserKnob {2 font}
 font C:/WINDOWS/Fonts/arial.ttf
 addUserKnob {18 fcolor l "font color" t "font color" R -1 1}
 fcolor 1
 addUserKnob {3 size l "font size" t "font size"}
 size 28
 addUserKnob {20 endGroup_2 l endGroup n -1}
 addUserKnob {20 scname l "scene name" t "scene name" n 1}
 addUserKnob {1 scene}
 addUserKnob {32 get_scene_name l "@b@C0xff000000@b get name" t "push this to get scene name from the read or write node" T "set n \[selected_node]\nif \{\[class \$n] == \"Read\" || \[class \$n] == \"Write\"\} \{\n\} else \{\n\t\terror \"please select READ or WRITE node\"\n\t\}\n\nset readfile \[filename \$n]\n\n\nset filetail \[file tail \$readfile] \nset fp \[string first . \$filetail]\nset strlen \[string length \$filetail]\nset lastp \[string last _ \$seqname]\n\nset scenename  \[string range \$filetail 0 \[expr \$fp-1]]\n\nknob scene  sc.\$scenename\n\n\n\n\n"}
 addUserKnob {1 tcframe l "framecode first frame" t "enter a framecode first frame and check the override box to change the source sequence framecode"}
 addUserKnob {6 framecode l override t "check this to change the source sequence framecode"}
 addUserKnob {20 endGroup n -1}
 addUserKnob {20 path l "output path" t "custom output paths" n 1}
 path 0
 addUserKnob {2 text_path l "text mov path" t "a directory to write a text mov to"}
 addUserKnob {2 clean_path l "clean mov path" t "a directory to write a clean mov to"}
 addUserKnob {6 pathov l "use custom paths" t "ckeck this to use custom output paths instead default"}
 addUserKnob {20 endGroup_6 l endGroup n -1}
 addUserKnob {20 filename t filename n 1}
 filename 0
 addUserKnob {1 txt_n l "text mov filename: sequencename +" t "text mov filename"}
 txt_n PAL
 addUserKnob {1 cln_n l "clean mov filename: sequencename +" t "clean mov filename"}
 cln_n PAL_clean
 addUserKnob {6 fignore l " ignore original sequence name" t "check this if you don't need original sequence name"}
 addUserKnob {20 endGroup_5 l endGroup n -1}
 addUserKnob {20 browse l "open in:" t "open in" n 1}
 browse 0
 addUserKnob {26 "" l "open in" T ""}
 addUserKnob {4 br l "" t "browser selection" M {explorer totalcmd}}
 addUserKnob {6 exp l " " t "check this to open a folder with the mov file in win explorer or totalcmd"}
 addUserKnob {1 totalcmd l totalcmd_path t "totalcmd path"}
 totalcmd C:/totalcmd/TOTALCMD.EXE
 addUserKnob {20 endGroup_1 l endGroup n -1}
 addUserKnob {20 mov l "mov settings" t "mov settings" n 1}
 mov 0
 addUserKnob {4 codec t "codec selection" M {Animation BMP Cinepak "Component Video" DV-PAL "DV/DVCPRO - NTSC" "DVCPRO - PAL" Graphics H.261 H.263 H.264 "Intel Indeo? Video 4.4" "JPEG 2000" "Motion JPEG A" "Motion JPEG B" "MPEG-4 Video" None "Photo - JPEG" "Planar RGB" PNG "Sorenson Video" "Sorensen Video 3" TGA TIFF Video}}
 codec "MPEG-4 Video"
 addUserKnob {7 fps t fps R 0 100}
 fps 25
 addUserKnob {4 quality t "quality selection" M {Min Low Normal High Max Lossless}}
 quality Lossless
 addUserKnob {20 endGroup_3 l endGroup n -1}
 addUserKnob {20 frmt l format t "reformat settings" n 1}
 frmt 0
 addUserKnob {1 format t "enter a format of the mov"}
 format "720 576 0 0 720 576 1.067 mov"
 addUserKnob {26 "" T " w h x y r t pixel_aspect name"}
 addUserKnob {20 endGroup_4 l endGroup n -1}
 addUserKnob {26 "" l ""}
 addUserKnob {26 "" T " @s-2 mov writer v0.1f  © cgpolis.com\n"}
 addUserKnob {32 help_1 l "@b@C0x89868100 help " T "message \"This node writes two .mov files from a selected read or write (you should have your sequence already rendered) node:\nwith text overlay (scene name in the left bottom and framecode in the right bottom corners (if box @b \\\"text\\\"@n checked)), and a clean one (if box @b \\\"clean\\\"@n checked).\nYou have to enter (or get) a @b scene name@n to write a \\\"text mov\\\" (you can enter space to write a \\\"text mov\\\" with framecode only.\nIf you push the @b@C0xff000000 \\\"get name\\\"@n button with the read node selected a script will get a @b scenename@n from an incoming sequence name.  \n\nYou can override an incoming sequence framecode by checking the box @b \\\"override\\\"@n and entering a @b \\\"framecode first frame\\\"@n\n\nYou can change the name of the final mov files in the filename group, check @b \\\"ignore original sequence name\\\"@n box to enter file names for text and clean movs,\notherwise this fields will be added to the source sequence name. \n\nYou can check the box in the @b \\\"open in\\\"@n group to load WIN explorer or total commander (please enter a valid path for totalcmd) \nto open the folder with the final mov files automaticly.\n\nThe final mov files by default are saved where the folder with the source sequence is located:\nfor examle if your sequence is: @b C:/Temp/scene/render/render.%04d.tif@n\nthe mov files will be: @b C:/Temp/scene/xxx.mov@n \nuse the @b \\\"output path\\\" @n group to change the directory to write mov files to\n\nplease send bugs and suggestions:\nmov \\@ cgpolis.com\"\n\n"}
}






set movxnode [knob [stack 0].name]
foreach n [nodes] {knob $n.selected false}
knob $movxnode.selected true
node_copy [cut_paste_file]
node_delete
foreach n [nodes] {knob $n.selected false}
node_paste [cut_paste_file]
foreach n [selected_nodes] {
knob $n.icon $movwriterdir/cgpdot.xpm
knob $n.plugdir "$movwriterdir"
}
#eval [concat autoplace [selected_nodes]]    
}