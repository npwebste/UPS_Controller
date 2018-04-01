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
import VFD_Modbus_Wrapper
import VFD_Modbus_Registers

def Run_Initialization():
	
	# Water
	
	# Solar
	
	
	# VFD
	#VFD.VFDInit("/dev/ttyUSB0".encode('ascii'),9600,8,1,1)
	VFD.VFDInit(Device.encode('ascii'),Baud,Data,Stop,ID)

	
	return 0