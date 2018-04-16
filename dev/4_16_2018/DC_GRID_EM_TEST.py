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
from PWM_Wrapper import *

# Declare Variables
# Main UPS Loop
while True:
	
	# Set parametersrameters and declare variables

	# Run initializtaion to setup VFD and converter controls
	Run_Initialization()
	# UPS Control Loop
	while True:
		#48-96
		# Vo = Vin*(1/(1-D))
		# Vo = Vin/D
		D = .6
		Val = 96*(1-D)
		PWM.PWM_Write(Parameters.Pin,int(Val))
		print(Parameters.Pin)
		time.sleep(5)