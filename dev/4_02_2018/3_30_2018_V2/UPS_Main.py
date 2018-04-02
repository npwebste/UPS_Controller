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
import Config
import time
import sqlite3
from VFD_Modbus_Wrapper import *
#import PWM_Wrapper

# Declare Variables
speed1 = 15
multiplier = 100

speed_mult = str(speed1*multiplier)
s1,s2 = speed_mult[:len(speed_mult)//2],speed_mult[len(speed_mult)//2:]
h = hex(int(s1)<<8|int(s2))
val = int(h,16)

# Main UPS Loop
while True:
	
    
    VFD.VFDInit("/dev/ttyUSB0".encode('ascii'),9600,8,1,1)
    
    time.sleep(5)
    VFD.VFDWrite(8192,1)
    time.sleep(10)
    t= VFD.VFDRead(269)
    print('Frequency is '+str(t/100))
    VFD.VFDWrite(269,3000)
    t= VFD.VFDRead(269)
    print('Frequency is ',t/100)
    time.sleep(10)
    VFD.VFDWrite(269,1500)
    t= VFD.VFDRead(269)
    print('Frequency is ',t/100)
    time.sleep(10) 
    VFD.VFDWrite(8192,3)
    time.sleep(15)
    
    VFD.VFDClose()
