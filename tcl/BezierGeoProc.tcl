#####################
#written by Frank Rueter
#last modified	Aug/22/2006
#this is used by BezierGeoTab.tcl to create geometric shapes with a Bezier node
#the following shapes are supported: circle, oval, square, rectangle, triangle.
#circle and square take into account the input's pixel aspect while oval, rectangle and triangle
#are absolute
#####################

proc BezierGeoProc {type} {
	in this {
	switch $type {
		rectangle {
			knob points {{
				"width/4 height/4"
				"width/4*3 height/4"
				"width/4*3 height/4*3"
				"width/4 height/4*3"
				}}
			knob center {{width/2} {height/2}}
			}
		square {
			knob points {{
				"(width/2-height/4)*pixel_aspect height/4"
				"(width/2+height/4)/pixel_aspect height/4"
				"(width/2+height/4)/pixel_aspect height/4*3"
				"(width/2-height/4)*pixel_aspect height/4*3"
				}}
			knob center {{width/2} {height/2}}
			}
		triangle {
			knob points {{
				"width/4 height/4"
				"width/4*3 height/4"
				"width/2 height/4*3"
				}}
			knob center {{width/2} {height/2}}
				}
		circle {
			knob points {{
				"width/2 height/4 pixel_aspect!=1?(height/7.3)/(pixel_aspect/2):height/7.3 0 pixel_aspect!=1?(height/7.3)/(pixel_aspect/2):height/7.3"
				"(width/2)+(height/4)/pixel_aspect height/2 height/7.3 1.57 height/7.3"
				"width/2 height/4*3 pixel_aspect!=1?(height/7.3)/(pixel_aspect/2):height/7.3 3.14 pixel_aspect!=1?(height/7.3)/(pixel_aspect/2):height/7.3"
				"(width/2)-(height/4)/pixel_aspect height/2 height/7.3 -1.57 height/7.3"
				}}
			knob center {{width/2} {height/2}}
			}
		oval {
			knob points {{
				"width/2 0 width/3.65*pixel_aspect 0 width/3.65*pixel_aspect"
				"width height/2 height/3.65 1.57 height/3.65"
				"width/2 height width/3.65*pixel_aspect 3.14 width/3.65*pixel_aspect"
				"0 height/2 height/3.65 -1.57 height/3.65"
				}}
			knob center {{width/2} {height/2}}
				}
		}
	knob label $type
	knob tile_color 99
	}
}