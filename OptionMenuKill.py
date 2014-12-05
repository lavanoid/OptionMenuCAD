#!/usr/bin/env python
import pifacecad
import time
import subprocess
import os,sys
import signal
from subprocess import call
cad = pifacecad.PiFaceCAD()
cd = os.path.dirname(os.path.realpath(sys.argv[0]))

# This is a daemon that checks if keys 0 to 4 are pressed. Once all their values are equal to 1 (pressed),
# it will kill all instances of python3. This is useful for when OptionMenu.py freezes.

while True:
		while True:
			keyspressed = cad.switches[0].value + cad.switches[1].value + cad.switches[2].value + cad.switches[3].value + cad.switches[4].value
			if keyspressed == 5:
				call([cd + "/OptionMenuKill"])
				time.sleep(5)