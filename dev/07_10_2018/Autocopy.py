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
# Import Libraries
import sqlite3
import shutil
import datetime
import csv
import os
from CSV_Manager import *
from UPS_Messages import *
cwd = os.getcwd()

print(cwd)

CSV_Write()

source = "/home/pi/datalogger/UPS_CSV.csv"

#destination = "/home/pi/datalogger/tmp/UPS_Export_%s.csv" % datetime.datetime.now().date()
destination = "/media/USB20FD/UPS_Export_%s.csv" % datetime.datetime.now().date()
print(destination)
try:
	shutil.copy2(source,destination)
except shutil.Error as e:
	print("Error: %s" % e)
	print("This one")
except IOError as e:
	print("Error: %s" % e.strerror)
	print("Second one")