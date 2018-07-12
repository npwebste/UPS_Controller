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

# Parameter configuration file for UPS controller

# Schedule interval in seconds
global PWM_Controller_Interval
global Protection_Controller_Interval
global VFD_Controller_Interval
global SCIP_Controller_Interval
global SQL_Database_Controller_Interval
global Archive_Controller_Interval

PWM_Controller_Interval = .5
Protection_Controller_Interval = 5
VFD_Controller_Interval = 15
SCIP_Controller_Interval = 60
SQL_Database_Controller_Interval = 5
Archive_Controller_Interval = 3600

# Water
global P_Min_Percent
global Theta_Max
P_Min_Percent = .5
Theta_Max = 60

# Solar
global P_Solar
P_Solar_Max = 1800

# Voltage Control
global DCLink_VDC_Max
global DCLink_VDC_Min
global Solar_VDC_Max
global Solar_VDC_Min
global Solar_Nominal
global Voltage_Multiplier
global D_Min
global D_Max
DCLink_VDC_Max = 350
DCLink_VDC_Min = 300
Solar_VDC_Max = 275
Solar_VDC_Min = 175
Solar_Nominal = 217.08
Voltage_Multiplier = .003330781
D_Min = .5
D_Max = .9

# VFD
global Device
global Baud
global Parity
global Data
global Stop
global ID
Device = "/dev/ttyUSB0"
Baud = 9600
Parity = "N"
Data = 8
Stop = 1
ID = 1


global VFD_Freq_Init
global VFD_Acc_Rate
global VFD_Freq_Max
global VFD_Volt_Max
global VFD_Amps_Max
global VFD_Power_Max
global VFD_BusVolt_Max
global VFD_Temp_Max
VFD_Freq_Init = 10
VFD_Acc_Rate = 1
VFD_Freq_Max = 61
VFD_Volt_Max = 240
VFD_Amps_Max = 15
VFD_Power_Max = 1800
VFD_BusVolt_Max = 400
VFD_Temp_Max = 40

# PWM
global PWMPin
global DigitalPin
global Output
global Mode
global Divisor
global Range
global PWM_Value

PWMPin = 26
AC_DigitalPin = 6
DC_DigitalPin = 5
Output = 'PWM_OUTPUT'
Mode = 'PWM_MODE_MS'
Divisor = 2
Range = 96

# PID
global P
global I
global D
global Voltage_Setpoint
global PID_Time
global PID_OLD_INIT

P = .001
I = .00005
D = 0
PID_Time = .01
Voltage_Setpoint = 325.269
PID_OLD_INIT = .8