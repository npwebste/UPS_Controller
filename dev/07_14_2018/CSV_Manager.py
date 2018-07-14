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

def CSV_Write(arg):
	try:
		conn = sqlite3.connect('UPS_DB.db')
		c = conn.cursor()
		csvdata = c.execute("SELECT * from UPS_DB")
		conn.close()
	except:
		logger.error('Could not read data from SQL database')

	with open('UPS_CSV.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(
			['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9'])
		writer.writerows(csvdata)
	csvfile.close()
	logger.info('CSV file successfully written')