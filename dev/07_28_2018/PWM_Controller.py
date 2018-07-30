# ©2018 The Arizona Board of Regents for and on behalf of Arizona State University and the Laboratory for Energy And Power Solutions, All Rights Reserved.
#
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
import VFD_Controller

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
PV_State = 0
N = 2

def PWM_Controller_Main(arg):

    # Setup PWM scheduler
    PWM_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the PWM controller and run
        PWM_Sched.enter(Parameters.PWM_Controller_Interval,1,PWM_Controller,("",))
        PWM_Sched.run()

def PWM_Controller(arg):
    global D_PID_OLD
    global Solar_Actual_Volts
    global DC_Link_Actual_Volts
    global N
    global PV_State

    # Get DC link voltage measurement and calculate actual value
    DC_Volts = PWM_Measure_Voltage('DC_Link')
    DC_Link_Actual_Volts = DC_Volts/Parameters.Voltage_Multiplier
    print("DC link voltage=", DC_Link_Actual_Volts)

    # Get solar measurement and calculate actual value
    Solar_Volts = PWM_Measure_Voltage('Solar')
    Solar_Actual_Volts = Solar_Volts/Parameters.Voltage_Multiplier
    print("Solar voltage=", Solar_Actual_Volts)

    if (Solar_Actual_Volts < Parameters.Solar_VDC_Max) and (Solar_Actual_Volts > Parameters.Solar_VDC_Min):
        # Calculate the updated DC-DC converter duty cycle
        DC_Relay(1)  # Set solar relay to closed position
        PV_State = 1
        D_PID = PWM_PID(DC_Link_Actual_Volts, D_PID_OLD)
        Convert = int(round(D_PID * Parameters.Range, 0))  # Convert to integer from float, value of 0 to 96
        PWM.PWM_Write(Parameters.PWMPin, Convert)
        D_PID_OLD = D_PID
        time.sleep(.5)
    else:
        logger.warning('Solar voltage out of acceptable range, cannot close in solar PV DC relay')
    time.sleep(.05)
    DC_Volts = PWM_Measure_Voltage('DC_Link')
    DC_Link_Actual_Volts = DC_Volts/Parameters.Voltage_Multiplier
    print('PWM DC UPdated is ',DC_Link_Actual_Volts)
    
    for n in range(N):
        if (DC_Link_Actual_Volts <= Parameters.DCLink_VDC_Min) or (DC_Link_Actual_Volts >= Parameters.DCLink_VDC_Max):
            time.sleep(.1)
            if n ==(N-1):
                PV_State = 0
                DC_Relay(0)  # Set solar relay to open
                logger.warning('DC link voltage out of acceptable range, opening solar PV DC relay ')
                time.sleep(5)  # Wait 5 seconds
        else:
            break
    # Update the duty cycle variable for the next iteration
    #D_PID_OLD = D_PID