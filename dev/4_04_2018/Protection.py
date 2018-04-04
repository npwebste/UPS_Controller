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

def ProtectionCheck():
	
	
	Float_Switch() # From float switch
	
	DC_Link_Voltage() # From inverter control card via SPI
	
	Inverter_Voltage() # From inverter control card via SPI
	
	Grid_Voltage() # Not needed, can measure from VFD input
	
	VFD_Freq_In()
	
	VFD_Voltage_In()
		
	VFD_Freq_Out()
	
	VFD_Voltage_Out()
	
	
	
	return 0