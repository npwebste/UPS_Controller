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


# Pin 11 (BCM 17) DC-DC
# Pin 13 (BCM 27) DC-AC
# Ground 9
def Fan_Control(Set_State):
	if Set_State = 1:
		PWM.Digital_Write(17,1)
		PWM.Digital_Write(27,1)
	else
		PWM.Digital_Write(17,0)
		PWM.Digital_Write(27,0)

	return 0