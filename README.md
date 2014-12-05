OptionMenuCAD
=============

This is a simple menu for the PiFace Control and Display (CAD). It has options to be able to stop and start services, run utilities, lock the screen, shutdown and reboot the system etc.

Installation
------------

The installation process is assuming that you have already installed all the PiFace CAD programs and that it has already been configured.

First, clone this repository using:

	git clone https://github.com/lavanoid/OptionMenuCAD
	
Secondly, make sure you have the PiFace CAD python libraries installed:
	
	sudo apt-get install python-pifacecad python3-pifacecad
	
Thirdly, set the file permissions:

	chmod 777 OptionMenuCAD -R

Finally, to run the script - just run this:

	cd OptionMenuCAD
	sudo ./OptionMenu.py
	
Configuring Utilities
---------------------

The OptionMenu.py may be able to execute just fine, however - not many of the functions are going to work. The services options are hard coded, if you don't have any of the services installed, you can manually modify the script and remove them - assuming you have some sort of python knowledge.

DroneKiller
-----------

The DroneKiller is a utility that causes the Parrot AR Drone to shutdown and crash (literally) - but only temporarily. The script is based on Hak5 Darren Kitchens proof of concept program.

To run DroneKiller - you need a wifi adapter (that isn't being used) and you'll need to install the following packages like so:
	
	sudo apt-get install telnet expect empty-expect
	
Pi-RC
-----

Pi-RC is a utility developed by Brandon Skari (with a few contributions from me) and is used to control RC Toys that operate on low frequency's, such as 27Mhz and 40Mhz. To install it, do the following:

	cd OptionMenuCAD
	git clone https://github.com/bskari/pi-rc
	sudo apt-get install scons libjansson-dev streamer
	cd pi-rc
	scons
	
That's it!

Initialising at boot
--------------------

You can configure your Pi to run this script at the end of the bootup sequence by modifying the rc.local file like so:

	sudo nano /etc/rc.local
	
The file should look something like this:

	#!/bin/sh -e
	#
	# rc.local
	#
	# This script is executed at the end of each multiuser runlevel.
	# Make sure that the script will "" on success or any other
	# value on error.
	#
	# In order to enable or disable this script just change the execution
	# bits.
	#
	# By default this script does nothing.

	# Print the IP address
	_IP=$(hostname -I) || true
	if [ "$_IP" ]; then
	  printf "My IP address is %s\n" "$_IP"
	fi

	sudo "/home/pi/OptionMenuCAD/OptionMenuKill.py" &
	sudo "/home/pi/OptionMenuCAD/OptionMenu.py" &
	sudo "/home/pi/OptionMenuCAD/shutdown_daemon" &
	exit 0

Want any help?
--------------

For any assistance, you can use everyone's friend Google or report an issue in this repo. Google is much preferred though.