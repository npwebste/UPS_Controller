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
import PID
import Parameters
from UPS_Error import *

DC_PID = PID.PID(Parameters.P, Parameters.I, Parameters.D)
DC_PID.setSampleTime(Parameters.PID_Time)
DC_PID.SetPoint = Parameters.Voltage_Setpoint

def PWM_PID(DC_Voltage,D_PID_OLD):
    DC_PID.update(DC_Voltage)
    D_update = DC_PID.output
    print("D_update = ",D_update)
    D = D_PID_OLD-D_update
    #print(D)
    if D > .8:
        D_out = .8
    elif D<.4:
        D_out = .4
    elif D<=.8 and D>=.4:
        D_out = D
    else:
        UPS_Error('Error_Duty_Cycle')
        print("ErrorD = ",D)
        D_out = .5
    #print(D_out)
    return D_out
