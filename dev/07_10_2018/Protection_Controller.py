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
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from PWM_Measure_Voltage import *
from Relay_Controller import *
from UPS_Messages import *

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
    Solar_Voltage = PWM_Measure_Voltage('Solar')/Parameters.Voltage_Multiplier # Measure solar volatge
    DC_Link_Voltage = PWM_Measure_Voltage('DC_Link')/Parameters.Voltage_Multiplier # Measure DC link voltage

    if (Solar_Voltage >= Parameters.Solar_VDC_Max or Solar_Voltage <= Parameters.Solar_VDC_Min):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3) # Stop motor
        Transfer_Switch(0) # Switch to grid source
        PWM.PWM_Write(Parameters.PWMPin,int(Parameters.PID_OLD_INIT*Parameters.Range)) # Reset PWM duty cycle to initial value
        DC_Relay(0) # Set solar relay to open
        UPS_Messages('Error_Solar_Voltage')

    if (DC_Link_Voltage >= Parameters.DCLink_VDC_Max or DC_Link_Voltage <= Parameters.DCLink_VDC_Min):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3) # Stop motor
        Transfer_Switch(0)  # Switch to grid source
        PWM.PWM_Write(Parameters.PWMPin,int(Parameters.PID_OLD_INIT*Parameters.Range)) # Reset PWM duty cycle to initial value
        DC_Relay(0) # Set solar relay to open position
        UPS_Messages('Error_DC_Link_Voltage')

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
        UPS_Error('Error_VFD_Freq')
    if (VFD_Volt >=Parameters.VFD_Volt_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Volt')
    if (VFD_Amps >=Parameters.VFD_Amps_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Amps')
    if (VFD_Power >=Parameters.VFD_Power_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Power')
    if (VFD_BusVolt >=Parameters.VFD_BusVolt_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_BusVolt')
    if (VFD_Temp >=Parameters.VFD_Temp_Max):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Temp')