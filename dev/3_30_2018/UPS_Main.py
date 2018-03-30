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
import PWM_Wrapper

# Declare Variables



# Main UPS Loop
while True:
	
	
	VFDInit("/dev/ttyUSB0",9600,8,1,1)
	time.sleep(5)
	VFDWrite(8192,1)
	time.sleep(5)
	VFDWrite(0269,7680)
	time.sleep(5)
	VFDWrite(8192,3)
	time.sleep(5)
	VFDClose()
	
	
	"""
	# Set parameters and declare variables
	Run_Config()
	print(Run_Config_Return)
	Initialize_Solar()
	
	Initialize_VFD()

	# UPS Control Loop
	while True:
		
		TankCheck()
		
		SolarMeasured()
		
		if P_Solar_Measured > P_Solar_Max*P_Min_Percent:
			setPWM()
			
			if startVFD() != 0:
				startVFD()
		
			setVFD()
			
			
		else
			setGrid()
			
			if startVFD() != 0:
				startVFD()
		
			setVFD()
		

		ProtectionCheck()
		"""
	
	
	
	
	

### SQL STUFF
#conn = sqlite3.connect('example.db')

#c = conn.cursor()

#c.execute('''CREATE TABLE Power(Date text, Voltage real, Current real, Power real)''')

#c.execute("INSERT INTO Power VALUES('2017',100,25,2500)")

#conn.commit()
#conn.close()
