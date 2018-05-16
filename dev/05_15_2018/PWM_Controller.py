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
import wiring
from PWM_Voltage_Measure import *

def PWM_Controller():

	DC_Volts = PWM_Voltage_Measure(DC_Link)

	D_PID = PWM_PID(DC_Volts)

	PWM_Output(D_PID)