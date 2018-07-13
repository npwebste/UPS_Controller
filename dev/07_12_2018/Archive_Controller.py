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
import sched
import time
import zipfile
import os
from datetime import datetime
import Parameters
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

def Archive_Controller_Main(arg):

    # Setup Archive scheduler
    Archive_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the SQL controller and run
        Archive_Sched.enter(Parameters.Archive_Controller_Interval, 1, Archive_Controller, ("",))
        Archive_Sched.run()

def Archive_Controller(arg):

    CSV_Write()

    # Create archive directory for current time
    Current_time = datetime.now()
    directory = '/home/pi/datalogger/Archive/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create archive
    zf_name = str(Current_time)+'_Archive'
    zf = zipfile.Zipfile(zf_name,'w')

    # Write files to zip archive and compress
    try:
        with zipfile.Zipfile(zf_name,'w') as zf:
            zf.write('UPS_DB.sql', zipfile.ZIP_STORED)# Write sql database to zip file
            zf.write('UPS_Messages.log', zipfile.ZIP_STORED)# Write log to zip file
            zf.write('UPS_DB.csv', zipfile.ZIP_STORED)# Write csv file to zip file

    except:
        logger.error('Could not write files to zip archive')

    try:
        os.remove('UPS_Messages.log')# Delete log file
        os.remove('UPS_DB.csv')# Delete csv file

        try:
            conn = sqlite3.connect('UPS_DB.db')
            c = conn.cursor()
            c.execute("DELETE FROM UPS_DB WHERE Date <= date('now','-1 day')")# Delete sql database older than one week
            conn.close()
        except:
            logger.error('Could not update SQL database')
    except:
        logger.error('Could not delete log and csv files')