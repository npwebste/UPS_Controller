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


def Error_Code():
	
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
	
	
	
	
	
	return