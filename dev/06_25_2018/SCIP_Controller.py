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
import Parameters
import sched
import time
#from PySCIPOpt import *

Solar_Power = 0

SCIP_Sched = sched.scheduler(time.time,time.sleep)

def SCIP_Controller(arg):
    global Solar_Power
    #SCIP_Power, SCIP_Freq = UPS_SCIP_Call()
    print("SCIP Called")
    SCIP_Sched.enter(30,1,SCIP_Controller,("",))
    SCIP_Sched.run()
    return SCIP_Power, SCIP_Freq