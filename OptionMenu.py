#!/usr/bin/env python3
import pifacecad
import time
import subprocess
import os,sys
import signal
from pifacecad.tools.question import LCDQuestion
from subprocess import call
cad = pifacecad.PiFaceCAD()
cd = os.path.dirname(os.path.realpath(sys.argv[0]))
dronekiller = "NotRunning"
hostapd_interface="wlan0"
hostapd_ipaddress="192.168.3.1"
while True:
	question = LCDQuestion(question="Option:", answers=["Services","Utilities","Shutdown","Reboot","Exit","Lock"])
	result = question.ask()
	if result == 0:
		# Services
		question = LCDQuestion(question="Service:", answers=["HOSTAPD","DNSMASQ","SAMBA", "Back"])
		result = question.ask()
		if result == 0:
			# Hostapd
			question = LCDQuestion(question="HOSTAPD Service", answers=["Start","Stop","Cancel"])
			result = question.ask()
			if result == 0:
				cad.lcd.clear()
				if dronekiller != "NotRunning":
					cad.lcd.write("DroneKiller\nis running!")
					time.sleep(2)
				else:
					cad.lcd.write("Starting HOSTAPD...")
					call(["service", "hostapd", "restart"])
					call(["ifconfig", hostapd_interface, hostapd_ipaddress])
			elif result == 1:
				cad.lcd.clear()
				cad.lcd.write("Stopping HOSTAPD...")
				call(["service", "hostapd", "stop"])
			# Hostapd end.
		elif result == 1:
			# DNSMASQ
			question = LCDQuestion(question="DNSMASQ Service", answers=["Start","Stop","Cancel"])
			result = question.ask()
			if result == 0:
				cad.lcd.clear()
				cad.lcd.write("Starting DNSMASQ...")
				## If the service is already running, then 'restart' should kill then start.
				call(["service", "dnsmasq", "restart"])
			elif result == 1:
				cad.lcd.clear()
				cad.lcd.write("Stopping DNSMASQ...")
				call(["service", "dnsmasq", "stop"])
			# DNSMASQ end.
		elif result == 2:
			# SAMBA
			question = LCDQuestion(question="SAMBA Service", answers=["Start","Stop","Cancel"])
			result = question.ask()
			if result == 0:
				cad.lcd.clear()
				cad.lcd.write("Starting SAMBA...")
				call(["service", "samba", "restart"])
			elif result == 1:
				cad.lcd.clear()
				cad.lcd.write("Stopping SAMBA...")
				call(["service", "samba", "stop"])
			# SAMBA end.
		# Services end.
	elif result == 1:
		# Utilities
		question = LCDQuestion(question="Utility:", answers=["Drone Killer","Pi-RC","Back"])
		result = question.ask()
		if result == 0:
			# Drone Killer
			question = LCDQuestion(question="Drone Killer:", answers=["Start","Stop","Cancel"])
			result = question.ask()
			if result == 0:
				question = LCDQuestion(question="AP will stop.", answers=["Continue","Cancel"])
				result = question.ask()
				if result == 0:
					cad.lcd.clear()
					cad.lcd.write("Stopping HOSTAPD...")
					call(["service", "hostapd", "stop"])
					if dronekiller != "NotRunning":
						cad.lcd.write("Already\nrunning!")
					else:
						cad.lcd.clear()
						# Kills a Parrot.AR Drone every 30 seconds.
						dronekiller = subprocess.Popen([cd + "/DroneKiller", "wlan0", "30", "192.168.1.1", "192.168.1.4"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
						cad.lcd.write("Killing drones...")
						#time.sleep(2)
						#line = dronekiller.stdout.readline()
						#if line !='':
						#	print(line.rstrip())
			elif result == 1:
				cad.lcd.clear()
				if dronekiller != "NotRunning":
					cad.lcd.write("Killing prog...")
					os.killpg(dronekiller.pid, signal.SIGTERM)
					time.sleep(2)
					dronekiller = "NotRunning"
				else:
					cad.lcd.write("Not running!")
					time.sleep(2)
		elif result == 1:
			question = LCDQuestion(question="Specification:", answers=["40 JSBR Mustang","27 JSBR Mustang","27 Pro Dirt","Cancel"])
			result = question.ask()
			if result == 0 or result == 1 or result == 2:
				if result == 0:
					configurationfile = cd + '/pi-rc/control-specs/jsbr-ford-mustang.json'
				elif result == 1:
					configurationfile = cd + '/pi-rc/control-specs/jsbr-ford-mustang-27mhz.json'
				elif result == 2:
					configurationfile = cd + '/pi-rc/control-specs/pro-dirt.json'
				cad.lcd.clear()
				pirc_pcm = subprocess.Popen([cd + "/pi-rc/pi_pcm"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
				call([cd + "/pi-rc/pifacecad_interactive_control.py", configurationfile])
				# Once 'pifacecad_interactive_control.py' has died, the pi_pcm server will also be killed.
				os.killpg(pirc_pcm.pid, signal.SIGTERM)
		# Utilities end.
	elif result == 4:
		cad.lcd.clear()
		cad.lcd.cursor_off()
		cad.lcd.write("Exiting...")
		time.sleep(3)
		cad.lcd.clear()
		cad.lcd.backlight_off()
		cad.lcd.display_off()
		exit()
	elif result == 5:
		# Lock
		cad.lcd.clear()
		cad.lcd.write("Locked!\nPress 0+4+5")
		cad.lcd.backlight_off()
		locked = True
		while locked == True:
			keyspressed = cad.switches[0].value + cad.switches[4].value + cad.switches[5].value
			if keyspressed == 3:
				locked = False
		#Lock end.
	elif result == 2:
		# Shutdown
		question = LCDQuestion(question="Shutdown?", answers=["Yes","No"])
		result = question.ask()
		if result == 0:
			cad.lcd.clear()
			cad.lcd.write("Shutting down...")
			time.sleep(2)
			call([cd + "/haltd"])
			cad.lcd.display_off()
			cad.lcd.backlight_off()
			exit()
		# Shutdown end.
	elif result == 3:
		# Reboot
		
		question = LCDQuestion(question="Reboot?", answers=["Yes","No"])
		result = question.ask()
		if result == 0:
			cad.lcd.clear()
			cad.lcd.write("Rebooting...")
			time.sleep(2)
			call([cd + "/rebootd"])
			cad.lcd.display_off()
			cad.lcd.backlight_off()
			exit()
		# Reboot end
