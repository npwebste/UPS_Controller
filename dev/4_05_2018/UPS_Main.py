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
#import Parameters
#from Parameters import *
import Parameters
from Initialization import *
import time
import sqlite3
#from VFD_Modbus_Wrapper import *
#import VFD_Modbus_Wrapper
#import VFD_Modbus_Registers
from PWM_Wrapper import *
from TransferSwitch import *


# Declare Variables

#

############
# 63 VD+
# 62 VD-
# 57 VAC +
# 58 VAC -
############

# Main UPS Loop
while True:
	
	# Set parametersrameters and declare variables
	print('Here first')
	print(Parameters.Pin)
	print(Parameters.Output)
	print(Parameters.Mode)
	print(Parameters.Divisor)
	print(Parameters.Range)
	# Run initializtaion to setup VFD and converter controls
	Run_Initialization()
	
	# UPS Control Loop
	while True:
		
		PWM.PWM_Write(Parameters.Pin,50)
		print(Parameters.Pin)
		time.sleep(5)
		
		Transfer_Switch(1)
		
		time.sleep(15)
		
		Transfer_Switch(0)
		
		
		
		#TankCheck()
		'''
		#SolarMeasured()
		#time.sleep(5)
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Frequency_Set"),1)
		time.sleep(10)
		t= VFD.VFDRead(269)
		print('Frequency is',t/100,'Hz')
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Frequency_Set"),3)
		time.sleep(15)
		'''
		'''
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
		'''

		#ProtectionCheck()
	

### SQL STUFF
#conn = sqlite3.connect('example.db')

#c = conn.cursor()

#c.execute('''CREATE TABLE Power(Date text, Voltage real, Current real, Power real)''')

#c.execute("INSERT INTO Power VALUES('2017',100,25,2500)")

#conn.commit()
#conn.close()