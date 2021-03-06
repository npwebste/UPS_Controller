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


VFD_Freq_Old = 0
Solar_State = 0
Grid_State = 0
Pump_State = 0
VFD_Counter = 0

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
    Solar_Voltage = Solar_Actual_Volts
    VFD_Power = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Power")) * 100

    if VFD_Power < Parameters.VFD_Operating_Min:
        VFD_Counter += 1
        if VFD_Counter > Parameters.VFD_Counter_Max:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
            Grid_State = 0
            Solar_State = 0
            Pump_State= 0
            logger.info('Pump is consuming no power, shutting down motor. Will try starting again in 5 minutes')
            time.sleep(Parameters.VFD_Wait)
            VFD_Counter = 0

    if Solar_Voltage > Parameters.Solar_VDC_Min:
        if Grid_State == 1:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
            logger.info('Previously running on grid. Shutting down motor to initialize solar PV source')
            time.sleep(10)
            Grid_State = 0
            Pump_State = 0
            VFD_Freq_Old = 0
        Transfer_Switch(1)
        time.sleep(1)
        if Pump_State == 0:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Acc"), int(500))
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
            Pump_State = 1
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(500))
        if Solar_Voltage > Parameters.Solar_VDC_Min :
            Freq_VFD = VFD_Freq_Old + 2
        elif Solar_Voltage <= (Parameters.Solar_VDC_Min-10):
            Freq_VFD = VFD_Freq_Old - 2
        else:
            logger.warning('Invalid solar voltage value')
        if Freq_VFD > Parameters.Solar_Freq_Max:
            Freq_VFD = Parameters.Solar_Freq_Max
        logger.info('Setting VFD to',Freq_VFD,' Hz from Solar PV power source')
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(Freq_VFD * 100))
        Solar_State = 1
    elif Solar_Voltage <= Parameters.Solar_VDC_Min and Solar_State ==1:
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.info('Solar voltage less than the accepable minimum, shutting down motor')
        time.sleep(10)
        Solar_State = 0
        Pump_State = 0
    else:
        logger.info('Setting to grid power, no solar available')

    if Solar_State == 0:
        Transfer_Switch(0)
        time.sleep(.1)
        Freq_VFD = Parameters.Grid_Freq_Max
        if Pump_State == 0:
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Acc"), int(100))
            VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 1)
            Pump_State = 1
        logger.info('Setting VFD to', Freq_VFD, ' Hz from grid power source')
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"), int(Freq_VFD * 100))
        Grid_State = 1
    else:
        logger.info('Solar power already enabled, will not enable grid')

    VFD_Freq_Old = Freq_VFD