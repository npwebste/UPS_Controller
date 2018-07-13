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

# Setup event logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('UPS_Event.log')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

CSV_Write()

source = "/home/pi/datalogger/UPS_CSV.csv"

#destination = "/home/pi/datalogger/tmp/UPS_Export_%s.csv" % datetime.datetime.now().date()
destination = "/media/USB20FD/UPS_Export_%s.csv" % datetime.datetime.now().date()
print(destination)
try:
	shutil.copy2(source,destination)
	logger.info('Data archive successfully transferred to USB')
except shutil.Error as e:
	print("Error: %s" % e)
	logger.error('Could not transfer data to USB')
except IOError as e:
	print("Error: %s" % e.strerror)
	logger.error('Could not transfer data to USB')