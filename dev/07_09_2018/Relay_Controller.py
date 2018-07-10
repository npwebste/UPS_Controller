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

# Transfer switch function to switch between solar and grid power source
def Transfer_Switch(Relay_State):
    if Relay_State == 1:
        PWM.Digital_Write(AC_DigitalPin,1) # Set solar power source
    elif Relay_State == 0:
        PWM.Digital_Write(AC_DigitalPin,0) # Set grid power source
    else:
        UPS_Error('Error_Transfer_Switch')
    return 0

def DC_Relay(Relay_State):
    if Relay_State == 1:
        PWM.Digital_Write(DC_DigitalPin, 1)  # Set solar relay in closed position
    elif Relay_State ==0:
        PWM.Digital_Write(DC_DigitalPin, 0)  # Set solar relay in open position
    else:
        UPS_Error('Error_DC_Relay')
    return 0