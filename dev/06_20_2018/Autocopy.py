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
import shutil
import datetime
import csv

conn = sqlite3.connect(UPS_DB)
c = conn.cursor()
csvdata = c.execute("SELECT * from UPS_DB")

with open('UPS_CSV.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	writer.writewrow(['Column1','Column2','Column3','Column4','Column5','Column6','Column7','Column8','Column9','Column10',])
	writer.writerows(data)


source = "/home/pi/UPS_CSV.csv"

destination = "/media/pi/USB1/UPS_Export_%s.csv" % datatime.datetime.now().date()

try:
	shutil.copy2(source,destination)
except shutil.Error as e:
	print("Error: %s" % e)
except IOError as e:
	print("Error: %s" % e.strerror)