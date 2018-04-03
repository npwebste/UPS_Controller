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
import PWM_Wrapper


# Pin 22 (BCM 25)
# Ground 20

def Fan_Control(Set_State):
	if Set_State = 1:
		Digital_Write(17,1)
	else
		Digital_Write(17,0)
	return 0