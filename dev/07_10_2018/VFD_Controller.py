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
import Parameters
import sched
import time
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from Relay_Controller import *
import SCIP_Controller

SCIP_Power = 0
SCIP_Freq = 0


def VFD_Controller_Main(arg):

    # Setup VFD scheduler
    VFD_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the VFD controller and run
        VFD_Sched.enter(Parameters.VFD_Controller_Interval, 1, VFD_Controller, ("",))
        VFD_Sched.run()

def VFD_Controller(arg):
    global SCIP_Power
    global SCIP_Freq
    # Measure Solar voltage

    # Measure solar current
    
    # Calculate solar power
    
    P_Solar = SCIP_Controller.Solar_Power

    if (P_Solar > 500):
        Transfer_Switch(0)
        print("TF0")
        time.sleep(.1)
        if (P_Solar >= SCIP_Power):
            P_VFD = SCIP_Power
        else:
            P_VFD = P_Solar
        if ((P_VFD/Parameters.P_Solar_Max)*Parameters.Theta_Max)<=SCIP_Freq:
            Freq_VFD = ((P_VFD/Parameters.P_Solar_Max)*Parameters.Theta_Max)
        else:
            Freq_VFD = SCIP_Freq
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
        time.sleep(.1)
        print("Freq_VFD=",Freq_VFD)
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(Freq_VFD*100))
    elif (P_Solar <= 500):
        Transfer_Switch(1)
        time.sleep(5)
        if (P_Solar >= SCIP_Power):
            P_VFD = SCIP_Power
        else:
            P_VFD = P_Solar
        if ((P_VFD / Parameters.P_Solar_Max) * Parameters.Theta_Max) <= SCIP_Freq:
            Freq_VFD = ((P_VFD / Parameters.P_Solar_Max) * Parameters.Theta_Max)
        else:
            Freq_VFD = SCIP_Freq
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
        time.sleep(2)
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(Freq_VFD*100))
    else:
        UPS_Error('Error_VFD_Power')