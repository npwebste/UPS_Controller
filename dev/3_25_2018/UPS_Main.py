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
import Config
import time
import sqlite3
import VFD_Modbus_Wrapper
#import PWM_Wrapper

# Declare Variables



# Main UPS Loop
while True:
	
	# Set parameters and declare variables
	Run_Config()
	print()
	Initialize_Solar()
	
	Initialize_VFD()
	
	f
	
	
	
	

### SQL STUFF
#conn = sqlite3.connect('example.db')

#c = conn.cursor()

#c.execute('''CREATE TABLE Power(Date text, Voltage real, Current real, Power real)''')

#c.execute("INSERT INTO Power VALUES('2017',100,25,2500)")

#conn.commit()
#conn.close()
