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
import Parameters
from Initialization import *
import time
import sqlite3
from VFD_Modbus_Wrapper import *
import VFD_Modbus_Registers
from PWM_Wrapper import *
from TransferSwitch import *


# Main UPS Loop
while True:
	
	# Set parametersrameters and declare variables
	# Run initializtaion to setup VFD and converter controls
	Run_Initialization()

	# UPS Control Loop
	while True:
		#time.sleep(5)
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Motor_Start_Stop"),1)
		time.sleep(10)
		t= VFD.VFDRead(269)
		print('Frequency is',t/100,'Hz')
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Motor_Start_Stop"),3)
		time.sleep(15)