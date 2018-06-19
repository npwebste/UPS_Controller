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
# Import Libraries
from PWM_Measure_Voltage import *
from PWM_PID import *
from PWM_Wrapper import *
D_PID_OLD = Parameters.PID_OLD_INIT


def PWM_Controller(D_PID_OLD):
    DC_Volts = PWM_Measure_Voltage('DC_Link')
    DC_Actual_Volts = DC_Volts/Parameters.Voltage_Multiplier
    print("Actual voltage=",DC_Actual_Volts)
    #print("OLD duty=",D_PID_OLD)

    D_PID = PWM_PID(DC_Volts,D_PID_OLD)
    print("Duty cyle=",D_PID)
    Convert = int(round(D_PID*96,0))
    #print("Actual voltage=",Convert)
    PWM.PWM_Write(Parameters.PWMPin,Convert)
    

    return D_PID
