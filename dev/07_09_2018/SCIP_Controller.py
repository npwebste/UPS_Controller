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
#from PySCIPOpt import *

Solar_Power = 0

def SCIP_Controller_Main(arg):

    # Setup SCIP scheduler
    SCIP_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the SCIP controller and run
        SCIP_Sched.enter(60, 1, SCIP_Controller, ("",))
        SCIP_Sched.run()

def SCIP_Controller(arg):
    global Solar_Power
    #SCIP_Power, SCIP_Freq = UPS_SCIP_Call()
    print("SCIP Called")
    Solar_Power = 0