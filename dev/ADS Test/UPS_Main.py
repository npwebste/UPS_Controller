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
from DC_PID import *
import ads1256

# Declare Variables

# Main UPS Loop
while True:
	
	# Set parametersrameters and declare variables
	# Run initializtaion to setup VFD and converter controls
	Run_Initialization()
	#PWM.PWM_Write(Parameters.Pin,96)
	# UPS Control Loop
	VFD.VFDWrite(,1)
	while True:
		
		Get_set = input('Enter Frequency Setpoint: ')
		print('Setting Frequency To: ',Get_set)
		time.sleep(1)
		if (Get_set < 50):
			VFD.VFD_VFDWrite(,)
		elif (Get_set >50)
			print('Input value too large, try again')
		
		ads1256.adc_read_channel(1)
		
	VFD.VFDWrite(,3)