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
import PWM_Controller
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from Relay_Controller import *
from PWM_Measure_Voltage import *

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


VFD_Freq_Old = 0 # Initial value for VFD frequency
Solar_State = 0 # State of the solar power source, 0 represents not being used, 1 represents being used
Grid_State = 0 # State of the grid power source, 0 represents not being used, 1 represents being used
Pump_State = 0# State of the water pumping, 0 represents not being used, 1 represents being used
VFD_Counter = 0 # Counter for VFD current level to monitor if the pump is being used

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
    global VFD_Freq_Old
    global Solar_State
    global Grid_State
    global Pump_State
    global VFD_Counter

    # Get DC link voltage measurement
    Solar_Voltage = PWM_Controller.Solar_Actual_Volts
    VFD_Amps = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Current")) / 100

    if VFD_Amps < Parameters.VFD_Operating_Min:
        VFD_Counter += 1
        if VFD_Counter > Parameters.VFD_Counter_Max:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
            Grid_State = 0
            Solar_State = 0
            Pump_State= 0
            VFD_Freq_Old = 0
            logger.info('Pump is consuming no power, shutting down motor. Will try starting again in 5 minutes')
            time.sleep(Parameters.VFD_Wait)
            VFD_Counter = 0

    # Check if solar power is available
    if (Solar_Voltage > Parameters.Solar_VDC_Min) and PWM_Controller.PV_State ==1:
        if Grid_State == 1:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
            logger.info('Previously running on grid. Shutting down motor to initialize solar PV source. Waiting 20 seconds')
            time.sleep(20)
            Grid_State = 0
            Pump_State = 0
            VFD_Freq_Old = 0
        Transfer_Switch(1) # Switch to solar PV source
        time.sleep(2)
        if Pump_State == 0:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
            time.sleep(2)
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Acc"), int(1000))
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
            Pump_State = 1
        #VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(100))
        if Solar_Voltage > Parameters.Solar_VDC_Min :
            Freq_VFD = VFD_Freq_Old + 2
        elif Solar_Voltage <= Parameters.Solar_VDC_Min:
            Freq_VFD = VFD_Freq_Old - 2
        else:
            logger.warning('Invalid solar voltage value')
        if Freq_VFD > Parameters.Solar_Freq_Max:
            Freq_VFD = Parameters.Solar_Freq_Max
        logger.info('VFD operating from Solar PV power source')
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(Freq_VFD * 100))
        Solar_State = 1
    elif Solar_Voltage <= Parameters.Solar_VDC_Min and Solar_State ==1:
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.info('Solar voltage less than the acceptable minimum, shutting down motor')
        time.sleep(10)
        Solar_State = 0
        Pump_State = 0
    else:
        logger.info('Setting to grid power, no solar available')

    # Use grid power if solar is unavailable
    if Solar_State == 0:
        Transfer_Switch(0)
        time.sleep(5)
        Freq_VFD = Parameters.Grid_Freq_Max
        if Pump_State == 0:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
            times.sleep(2)
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Acc"), int(500))
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
            Pump_State = 1
        logger.info('VFD operating from grid power source')
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(Freq_VFD * 100))
        Grid_State = 1
    else:
        logger.info('Solar power already enabled, will not enable grid')

    VFD_Freq_Old = Freq_VFD