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
import Parameters
import sched
import time
import logging
#from PySCIPOpt import *

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

Solar_Power = 0

def SCIP_Controller_Main(arg):

    # Setup SCIP scheduler
    SCIP_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the SCIP controller and run
        SCIP_Sched.enter(Parameters.SCIP_Controller_Interval, 1, SCIP_Controller, ("",))
        SCIP_Sched.run()

def SCIP_Controller(arg):
    global Solar_Power
    #SCIP_Power, SCIP_Freq = UPS_SCIP_Call()
    Solar_Power = 0