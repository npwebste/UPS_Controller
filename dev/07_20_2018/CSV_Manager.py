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

def CSV_Write():
    try:
        conn = sqlite3.connect('UPS_DB.db')
        c = conn.cursor()
        csvdata = c.execute("SELECT * from UPS_DB")
        conn.close()
        with open('UPS_CSV.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Solar Voltage', 'DC Link Voltage', 'Duty Cycle', 'VFD Frequency', 'VFD Voltage', 'VFD Amps','VFD Power', 'Grid Power', 'Solar Power', 'VFD Bus Voltage', 'VFD Temperature'])
            writer.writerows(csvdata)
        csvfile.close()
        conn.close()
        logger.info('CSV file successfully written')
    except:
        logger.error('Could not read data from SQL database')

