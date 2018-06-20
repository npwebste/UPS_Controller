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
import time
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from PWM_Measure_Voltage import *
from UPS_Error import *

def Protection_Controller():
    # Check Solar setpoints
    Solar_Voltage = PWM_Measure_Voltage('Solar')
    DC_Link_Voltage = PWM_Measure_Voltage('DC_Link')
    if (Solar_Voltage >=Parameters.SolarMax):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        PWM_Output(Parameters.PWMPin,0)
        UPS_Error('Error_Solar_Voltage')
    if (DC_Link_Voltage >= Parameters.DCLinkMax):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        PWM_Output(Parameters.PWMPin, 0)
        UPS_Error('Error_DC_Link_Voltage')
    # Check Grid setpoints

    # Check VFD setpoint
    VFD_Freq = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Frequency"))/100
    VFD_Volt = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Voltage"))
    VFD_Amps = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Current"))/100
    VFD_Power =VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Power"))/10
    VFD_BusVolt = VFD.VFDRead(reg.get("ReadFunc",{}).get("Bus_Voltage"))
    VFD_Temp = VFD.VFDRead(reg.get("ReadFunc",{}).get("Temperature"))

    if (VFD_Freq >=61):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Freq')
    if (VFD_Volt >=240):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Volt')
    if (VFD_Amps >=15):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Amps')
    if (VFD_Power >=2000):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Power')
    if (VFD_BusVolt >=400):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_BusVolt')
    if (VFD_Temp >=40):
        VFD.VFDWrite(reg.get("WriteFunc", {}).get("Motor_Start_Stop"), 3)
        UPS_Error('Error_VFD_Temp')