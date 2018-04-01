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


def Set_Parameters():
	
	# Water
	global P_Min_Percent
	P_Min_Percent = .5
	
	# Solar
	global P_Solar
	P_Solar = 2500
	
	
	# VFD
	global Device
	global Baud
	global Parity
	global Data
	global Stop
	global ID
	
	Device = "/dev/ttyUSB0"
	Baud = 9600
	Parity = "N"
	Data = 8
	Stop = 1
	ID = 1
	
	# PWM
	global Pin
	global Output
	global Mode
	global Divisor
	global Range
	global PWM_Value
	
	Pin =1
	Output = 'PWM_OUTPUT'
	Mode = 'PWM_MODE_MS'
	Divisor = 2
	Range = 96
		
	
	
	
	return 0