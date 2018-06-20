# Universal Power Supply Controller
# USAID Middle East Water Security Initiative
#
# Developed by: Nathan Webster
# Primary Investigator: Nathan Johnson
#
# Version History (mm_dd_yyyy)
# 1.00 03_24_2018_NW
#
######################################################
# Import Libraries
import sqlite3
import shutil
import datetime
import csv
import os
cwd = os.getcwd()

print(cwd)

conn = sqlite3.connect('UPS_DB.db')
c = conn.cursor()
csvdata = c.execute("SELECT * from UPS_DB")


with open('UPS_CSV.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Column1','Column2','Column3','Column4','Column5','Column6','Column7','Column8','Column9'])
	writer.writerows(csvdata)
csvfile.close()

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