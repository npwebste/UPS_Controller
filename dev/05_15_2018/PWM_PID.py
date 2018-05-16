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
import ads1256
import PID
import Parameters

def PWM_PID(DC_Voltage):

	DC_PID = PID.PID(Parameters.P, Parameters.I, Parameters.D)
	DC_PID.SetPoint(Parameters.Voltage_Setpoint)

    D = DC_PID.feedback(DC_Voltage)

	return D