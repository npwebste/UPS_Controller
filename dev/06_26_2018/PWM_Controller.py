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

D_PID_OLD = Parameters.PID_OLD_INIT
PWM_Sched = sched.scheduler(time.time,time.sleep)

def PWM_Controller(arg):
    global D_PID_OLD
    #ST = time.time()
    DC_Volts = PWM_Measure_Voltage('DC_Link')
    DC_Actual_Volts = DC_Volts/Parameters.Voltage_Multiplier
    print("Actual voltage=",DC_Actual_Volts)
    D_PID = PWM_PID(DC_Actual_Volts,D_PID_OLD)
    print("Duty cyle=",D_PID)
    Convert = int(round(D_PID*96,0))
    PWM.PWM_Write(Parameters.PWMPin,Convert)
    D_PID_OLD = D_PID
    #ET=time.time()
    #Diff = ET-ST
    #print(Diff)
    PWM_Sched.enter(.01,1,PWM_Controller,("",))
    PWM_Sched.run()