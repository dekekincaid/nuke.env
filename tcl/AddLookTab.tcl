#written by frankr + broesler
#last update Nov 30th 2007
###################
# this adds a tab to make a camera always look at another object
###################
proc AddLookTab {} {
	addUserKnob node [stack 0] 20 Look
	addUserKnob node [stack 0] 32 "" l "look at" T "set lookAt \[value lookObject]\nputs \$lookAt\nset xX \"degrees(atan2(\$lookAt.translate.y-translate.y,sqrt(pow(\$lookAt.translate.x-translate.x,2)+pow(\$lookAt.translate.z-translate.z,2))))\"\nset yX \"\$lookAt.translate.z-this.translate.z >= 0 ? 180+degrees(atan2(\$lookAt.translate.x-translate.x,\$lookAt.translate.z-translate.z)):180+degrees(atan2(\$lookAt.translate.x-translate.x,\$lookAt.translate.z-translate.z))\"\nin this.rotate.x \{set_expression \$xX\}\nin this.rotate.y \{set_expression \$yX\}"
	addUserKnob node [stack 0] 1 lookObject l ""
	}
