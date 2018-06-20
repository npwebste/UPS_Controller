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
# Water
global P_Min_Percent
P_Min_Percent = .5

global Theta_Max
Theta_Max = 60

global DCLinkMax
global SolarMax
DCLinkMax = 350
SolarMax = 275


# Solar
global P_Solar

P_Solar_Max = 1800

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

# PWM
global PWMPin
global DigitalPin
global Output
global Mode
global Divisor
global Range
global PWM_Value

PWMPin =23
DigitalPin = 6
Output = 'PWM_OUTPUT'
Mode = 'PWM_MODE_MS'
Divisor = 2
Range = 96

global D_Min
global D_Max

global Duty

Duty = .5

# PID
global P
global I
global D
global Voltage_Setpoint
global PID_Time
global Voltage_Multiplier
global PID_OLD_INIT

P = .001
I = .01
D = 0
PID_Time = .01
#Voltage_Setpoint = 325.3
Voltage_Setpoint = 40
Voltage_Multiplier = .003330781
PID_OLD_INIT = .6