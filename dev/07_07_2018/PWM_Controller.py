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
import sched
import time
from PWM_Measure_Voltage import *
from PWM_PID import *
from PWM_Wrapper import *
from Relay_Controller import *
from UPS_Error import *

# Define initial duty cycle value
D_PID_OLD = Parameters.PID_OLD_INIT

# Setup PWM scheduler
PWM_Sched = sched.scheduler(time.time,time.sleep)

def PWM_Controller(arg):
    global D_PID_OLD

    # Get DC link voltage measurement and calculate actual value
    DC_Volts = PWM_Measure_Voltage('DC_Link')
    DC_Link_Actual_Volts = DC_Volts/Parameters.Voltage_Multiplier
    print("DC link voltage=", DC_Actual_Volts)
    # Get DC link voltage measurement and calculate actual value
    Solar_Volts = PWM_Measure_Voltage('Solar')
    Solar_Actual_Volts = Solar_Volts/Parameters.Voltage_Multiplier

    if (Solar_Actual_Volts <= Parameters.DCLink_VDC_Min) and (Solar_Actual_Volts >= Parameters.DCLink_VDC_Max):
        DC_Relay(0)# Set solar relay to open
        time.sleep(10) # Wait 10 seconds
    elif Solar_Actual_Volts (DC_Actual_Volts > Parameters.DCLink_VDC_Min) and (Solar_Actual_Volts < Parameters.DCLink_VDC_Max):
        DC_Relay(1) # Set solar relay to closed position
        time.sleep(5) # Wait 5 seconds
    else:
        UPS_Error('Error_Solar_Voltage_Relay')

    # Calculate the updated DC-DC converter duty cycle
    D_PID = PWM_PID(DC_Link_Actual_Volts,D_PID_OLD)
    print("Duty cyle=",D_PID)
    Convert = int(round(D_PID*Parameters.Range,0)) # Convert to integer from float, value of 0 to 96
    PWM.PWM_Write(Parameters.PWMPin,Convert)

    # Update the duty cycle variable for the next iteration
    D_PID_OLD = D_PID

    # Reschedule the PWM controller and run
    PWM_Sched.enter(.5,1,PWM_Controller,("",))
    PWM_Sched.run()