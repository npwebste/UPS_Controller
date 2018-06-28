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
from threading import Thread
from PWM_Controller import *
from Protection_Controller import *
from VFD_Controller import *
from SCIP_Controller import *
from SQL_Database import *
from Initialization import *
# Declare Variables

# Run initialization to setup VFD and converter controls
print("Beginning controller initilization")
Run_Initialization()
print("Initialization complete")

# UPS Control Threads
PWM_Thread = Thread(target=PWM_Controller, args=("",))
Protection_Thread = Thread(target=Protection_Controller, args=("",))
VFD_Thread = Thread(target=VFD_Controller, args=("",))
SCIP_Thread = Thread(target=SCIP_Controller, args=("",))
SQL_Thread = Thread(target=SQL_Database, args=("",))

PWM_Thread.start()
Protection_Thread.start()
VFD_Thread.start()
SCIP_Thread.start()
SQL_Thread.start()