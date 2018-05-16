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
global Pin
global Output
global Mode
global Divisor
global Range
global PWM_Value

PWMPin = 1
DigitalPin = 5
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

P = .1
I = 0
D = 0
Voltage_Setpoint = 325.3