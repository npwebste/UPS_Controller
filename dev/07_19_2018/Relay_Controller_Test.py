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
import time

# Setup event logging

# Pin 22 (BCM 25)
# Ground 20
PWM.PWM_Setup()
PWM.PWM_Pin_Mode(Parameters.PWMPin)
PWM.PWM_Set_Mode()
PWM.PWM_Set_Clock(Parameters.Divisor)
PWM.Pin_Mode_Output(Parameters.AC_DigitalPin)
PWM.Pin_Mode_Output(Parameters.DC_DigitalPin)

PWM.Digital_Write(Parameters.AC_DigitalPin,1) # Set solar power source
time.sleep(5)
PWM.Digital_Write(Parameters.AC_DigitalPin,0) # Set grid power source
time.sleep(5)
PWM.Digital_Write(Parameters.DC_DigitalPin, 1)  # Set solar relay in closed position
time.sleep(5)
PWM.Digital_Write(Parameters.DC_DigitalPin, 0)  # Set solar relay in open position