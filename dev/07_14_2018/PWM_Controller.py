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
import logging
from PWM_Measure_Voltage import *
from PWM_PID import *
from PWM_Wrapper import *
from Relay_Controller import *

# Setup event logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('UPS_Event.log')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Define initial duty cycle value
D_PID_OLD = Parameters.PID_OLD_INIT

def PWM_Controller_Main(arg):

    # Setup PWM scheduler
    PWM_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the PWM controller and run
        PWM_Sched.enter(Parameters.PWM_Controller_Interval,1,PWM_Controller,("",))
        PWM_Sched.run()

def PWM_Controller(arg):
    global D_PID_OLD

    # Get DC link voltage measurement and calculate actual value
    DC_Volts = PWM_Measure_Voltage('DC_Link')
    DC_Link_Actual_Volts = DC_Volts/Parameters.Voltage_Multiplier
    print("DC link voltage=", DC_Link_Actual_Volts)
    # Get solar measurement and calculate actual value
    Solar_Volts = PWM_Measure_Voltage('Solar')
    Solar_Actual_Volts = Solar_Volts/Parameters.Voltage_Multiplier

    if (DC_Link_Actual_Volts <= Parameters.DCLink_VDC_Min) and (DC_Link_Actual_Volts >= Parameters.DCLink_VDC_Max):
        DC_Relay(0)# Set solar relay to open
        time.sleep(10) # Wait 10 seconds
    elif (DC_Link_Actual_Volts > Parameters.DCLink_VDC_Min) and (DC_Link_Actual_Volts < Parameters.DCLink_VDC_Max):
        DC_Relay(1) # Set solar relay to closed position
        time.sleep(5) # Wait 5 seconds
    else:
        logger.warning('Solar voltage out of accecptable range, cannot turn on solar relay')

    # Calculate the updated DC-DC converter duty cycle
    D_PID = PWM_PID(DC_Link_Actual_Volts,D_PID_OLD)
    print("Duty cyle=",D_PID)
    Convert = int(round(D_PID*Parameters.Range,0)) # Convert to integer from float, value of 0 to 96
    PWM.PWM_Write(Parameters.PWMPin,Convert)

    # Update the duty cycle variable for the next iteration
    D_PID_OLD = D_PID