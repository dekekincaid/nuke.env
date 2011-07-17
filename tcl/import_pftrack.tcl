proc import_pftrack {} {


global env
panel {import pftrack} {
    {"geo file: " geofile f}
    {"clipfile: " clipfile f}
    }
 regsub -all {\\} "$clipfile" "/" clipfile
 regsub -all {\\} "$geofile" "/" geofile
 #puts "$geofile \n$clipfile"
 
 ####replace the python stuff here with yours
 
  set pyscript "the/path/to/the/pftrack2nuke.py"
  set pythonoPath "YOURPYTHONPATH/eg/C:/tools/Python24/python.exe"
  eval [exec $pythonoPath $pyscript -c $clipfile -g $geofile]
 }
