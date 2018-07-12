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
from UPS_Messages import *

def CSV_Write(arg):
	try:
		conn = sqlite3.connect('UPS_DB.db')
		c = conn.cursor()
		csvdata = c.execute("SELECT * from UPS_DB")
		conn.close()
	except:
		UPS_Messages('CSV Error')

	with open('UPS_CSV.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(
			['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9'])
		writer.writerows(csvdata)
	csvfile.close()