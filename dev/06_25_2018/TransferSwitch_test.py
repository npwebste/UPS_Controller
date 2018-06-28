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
from PWM_Wrapper import *
import time
import Parameters
# Pin 22 (BCM 25)
# Ground
#PWM.PWM_Setup()
#PWM.Pin_Mode_Output(6)
PWM.PWM_Setup()
PWM.PWM_Pin_Mode(Parameters.PWMPin)
PWM.PWM_Set_Mode()
PWM.PWM_Set_Clock(Parameters.Divisor)
PWM.Pin_Mode_Output(6)
PWM.PWM_Set_Range(Parameters.Range)
while 1:
    PWM.PWM_Write(Parameters.PWMPin,48)
    PWM.Digital_Write(6,1)
    print("Now on")
    time.sleep(3)
    PWM.Digital_Write(6,0)
    print("Now off")
    time.sleep(3)

