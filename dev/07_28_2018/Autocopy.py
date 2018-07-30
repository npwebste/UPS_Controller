# ©2018 The Arizona Board of Regents for and on behalf of Arizona State University and the Laboratory for Energy And Power Solutions, All Rights Reserved.
#
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
import logging
from Archive_Controller import *

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

Archive_Controller(("",))

source = '/home/pi/datalogger/Archive'
# destination = "/home/pi/datalogger/tmp/UPS_Export_%s.csv" % datetime.datetime.now().date()
destination = "/media/USB20FD/UPS_Export_%s" % datetime.datetime.now().date()
# os.makedir
# if not os.path.exists(destination):
#        os.makedirs(destination)
try:
    if not os.path.exists(destination):
        os.makedirs(destination, 0o777)
        os.chmod(destination, 0o777)
    src_files = os.listdir(source)
    for file_name in src_files:
        full_file_name = os.path.join(source, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, destination)
    logger.info('Data archive successfully transferred to USB')
except shutil.Error as e:
    print("Error: %s" % e)
    logger.error('Could not transfer data to USB')
except IOError as e:
    print("Error: %s" % e.strerror)
    logger.error('Could not transfer data to USB')
