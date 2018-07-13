#!/bin/sh

# Universal Power System Controller
# USAID Middle East Water Security Initiative
#
# Developed by: Nathan Webster
# Primary Investigator: Nathan Johnson
#
# Version History (mm_dd_yyyy)
# 1.00 07_13_2018_NW
#
######################################################
cd /
cd /home/pi/datalogger
mkdir /home/pi/datalogger/tmp
sleep 3
sudo /usr/bin/python3 Autocopy.py
sleep 5
#umount /media/pi/USB20FD
cd /
exit