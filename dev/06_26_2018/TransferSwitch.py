# Universal Power System Controller
# USAID Middle East Water Security Initiative
#
# Developed by: Nathan Webster
# Primary Investigator: Nathan Johnson
#
# Version History (mm_dd_yyyy)
# 1.00 07_13_2018_NW
#
######################################################
from PWM_Wrapper import *
import Parameters

# Pin 22 (BCM 25)
# Ground 20

def Transfer_Switch(Set_State):
    if Set_State == 1:
        PWM.Digital_Write(6,1)
    elif Set_State == 0:
        PWM.Digital_Write(6,0)
    else:
        UPS_Error('Error_Transfer_Switch')
    return 0
