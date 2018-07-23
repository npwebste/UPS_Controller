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
from threading import Thread
from PWM_Controller import *
from Protection_Controller import *
from VFD_Controller import *
from SCIP_Controller import *
from SQL_Database_Controller import *
from Archive_Controller import *
from Initialization import *
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
import Parameters

# Declare Variables

# Run initialization to setup VFD and converter controls
Run_Initialization()

# UPS Control Threads
#PWM_Thread = Thread(target=PWM_Controller_Main, args=("",))
#Protection_Thread = Thread(target=Protection_Controller_Main, args=("",))
#VFD_Thread = Thread(target=VFD_Controller_Main, args=("",))
#SCIP_Thread = Thread(target=SCIP_Controller_Main, args=("",))
#SQL_Thread = Thread(target=SQL_Database_Controller_Main, args=("",))
#Archive_Thread = Thread(target=Archive_Controller_Main,args=("",))

#PWM_Thread.start()
#Protection_Thread.start()
#VFD_Thread.start()
#SCIP_Thread.start()
#SQL_Thread.start()
#Archive_Thread.start()

VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
time.sleep(5)
VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(10*100))
time.sleep(5)
VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(20*100))
time.sleep(5)
VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(30*100))
time.sleep(5)
VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(35*100))
VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
