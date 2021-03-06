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
import VFD_Controller
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from Relay_Controller import *

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

# Setup protection scheduler
Protection_Sched = sched.scheduler(time.time,time.sleep)

def Protection_Controller_Main(arg):
    # Setup Protection scheduler
    Protection_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the Protection controller and run
        Protection_Sched.enter(Parameters.Protection_Controller_Interval, 1, Protection_Controller, ("",))
        Protection_Sched.run()

def Protection_Controller(arg):

    # Check Solar
    time.sleep(.01) # Wait .01 seconds to prevent segmentation fault
    Solar_Voltage = PWM_Controller.Solar_Actual_Volts
    DC_Link_Voltage = PWM_Controller.DC_Link_Actual_Volts

    if (Solar_Voltage >= Parameters.Solar_VDC_Max or Solar_Voltage <= Parameters.Solar_VDC_Min) and (VFD_Controller.Solar_State ==1):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3) # Stop motor
        logger.warning('Solar PV voltage out of acceptable range, shutting down motor')
        Transfer_Switch(0) # Switch to grid source
        logger.warning('Solar PV voltage out of acceptable range,,setting transfer relay to grid power source')
        PWM.PWM_Write(Parameters.PWMPin,int(Parameters.PID_OLD_INIT*Parameters.Range)) # Reset PWM duty cycle to initial value
        DC_Relay(0) # Set solar relay to open
        logger.warning('Solar PV voltage out of acceptable range, opening solar PV DC relay')

    if (DC_Link_Voltage >= Parameters.DCLink_VDC_Max or DC_Link_Voltage <= Parameters.DCLink_VDC_Min) and (VFD_Controller.Solar_State ==1):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3) # Stop motor
        logger.warning('DC link voltage out of acceptable range, shutting down motor')
        Transfer_Switch(0)  # Switch to grid source
        logger.warning('DC link voltage out of acceptable range,,setting transfer relay to grid power source')
        PWM.PWM_Write(Parameters.PWMPin,int(Parameters.PID_OLD_INIT*Parameters.Range)) # Reset PWM duty cycle to initial value
        DC_Relay(0) # Set solar relay to open position
        logger.warning('DC link voltage out of acceptable range, opening solar PV DC relay')

    # Check Grid

    # Check VFD
    VFD_Freq = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Frequency"))/100
    VFD_Volt = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Voltage"))
    VFD_Amps = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Current"))/100
    VFD_Power =VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Power"))/10
    VFD_BusVolt = VFD.VFDRead(reg.get("ReadFunc",{}).get("Bus_Voltage"))
    VFD_Temp = VFD.VFDRead(reg.get("ReadFunc",{}).get("Temperature"))

    if (VFD_Freq >=Parameters.VFD_Freq_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.warning('VFD frequency set above maximum, shutting down motor')
    if (VFD_Volt >=Parameters.VFD_Volt_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.warning('VFD votlage set above maximum, shutting down motor')
    if (VFD_Amps >=Parameters.VFD_Amps_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.warning('VFD current set above maximum, shutting down motor')
    if (VFD_Power >=Parameters.VFD_Power_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.warning('VFD power set above maximum, shutting down motor')
    if (VFD_BusVolt >=Parameters.VFD_BusVolt_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.warning('VFD bus voltage set above maximum, shutting down motor')
    if (VFD_Temp >=Parameters.VFD_Temp_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        logger.warning('VFD temperature set above maximum, shutting down motor')