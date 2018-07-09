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
import PID
import Parameters
from UPS_Error import *

DC_PID = PID.PID(Parameters.P, Parameters.I, Parameters.D)
DC_PID.setSampleTime(Parameters.PID_Time)
DC_PID.SetPoint = Parameters.Voltage_Setpoint

def PWM_PID(DC_Voltage,D_PID_OLD):
    DC_PID.update(DC_Voltage) # Run the PID update function
    D_update = DC_PID.output # Get the updated PID duty cycle value
    D = D_PID_OLD-D_update # Calculate the change in the duty cycle

    # Duty cycle protection statement to ensure acceptable operating range
    if D > Parameters.D_Max:
        D_out = Parameters.D_Max
    elif D < Parameters.D_Min:
        D_out = Parameters.D_Min
    elif D <= Parameters.D_Max and D >= Parameters.D_Min:
        D_out = D
    else:
        UPS_Error('Error_Duty_Cycle')
        D_out = Parameters.PID_OLD_INIT # Reset duty cycle to default initial value
    return D_out