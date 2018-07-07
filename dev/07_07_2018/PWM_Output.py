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
# Import Libraries
from PWM_Wrapper import *
import Parameters

def PWM_Output(D_PID):

    PWM_Write(Parameters.PWMPin,D_PID)