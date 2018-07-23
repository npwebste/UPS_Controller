#!/bin/sh

# ©2018 The Arizona Board of Regents for and on behalf of Arizona State University and the Laboratory for Energy And Power Solutions, All Rights Reserved.
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
mkdir /home/pi/datalogger
sleep 2
sudo /usr/bin/python3 /home/xyz/Autocopy.py
sleep 5
#umount /media/pi/USB20FD
cd /
exit