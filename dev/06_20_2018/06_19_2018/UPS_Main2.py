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
import sched,time
from UPS_Sched import *
from PWM_Controller import *
from Protection_Controller import *
from VFD_Controller import *
#from SCIP_Controller import *
from SQL_Database import *
from Initialization import *
# Declare Variables
SCIP_VFD = 0
SCIP_Power = 0
s = sched.scheduler(time.time, time.sleep)
# Main UPS Loop
while True:
    # Run initializtaion to setup VFD and converter controls
    
    print("Beginning controllier initilization")
    Run_Initialization()
    print("Initialization complete")
     # UPS Control Loop
    while True:
        PWM_Thread(s, 1, PWM_Controller, ())
        #print("Hey i got here",t)

        Protection_Thread(s, 5, Protection_Controller, ())

        #VFD_Thread(s, 10, VFD_Controller, SCIP_Power, SCIP_VFD)

        #SCIP_Power, SCIP_VFD = SCIP_Thread(s, 300, SCIP_Controller(), )

        SQL_Thread(s, 60, SQL_Database, ())
        
        s.run()