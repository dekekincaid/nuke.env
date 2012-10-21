import nuke
def nodePresetsStartup():
  nuke.setUserPreset("Grade", "grade", {'black_clamp': 'false', 'whitepoint': '2.4', 'selected': 'true', 'black': '-0.215', 'multiply': '2.04', 'white': '2.12'})
