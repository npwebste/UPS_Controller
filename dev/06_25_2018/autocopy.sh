#!/bin/sh
cd /
cd /home/pi/datalogger
mkdir /home/pi/datalogger/tmp
sleep 3
sudo /usr/bin/python3 Autocopy.py
sleep 5
#umount /media/pi/USB20FD
cd /
exit