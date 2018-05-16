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
import ads1256
from UPS_Error import *

def PWM_Voltage_Measure(Measurement):
    gain = 1  # ADC's Gain parameter
    sps = 25  # ADC's SPS parameter
    ads1256.start(str(gain), str(sps))

    if Measurement == 'DC_Link':
        ChannelValue = ads1256.read_channel(3)
        ChannelValueVolts = (((ChannelValue * 100) / 167.0) / int(gain)) / 1000000.0
        DCVolts = ChannelValueVolts
    elif Measuremnet == 'Solar':
        ChannelValue = ads1256.read_channel(3)
        ChannelValueVolts = (((ChannelValue * 100) / 167.0) / int(gain)) / 1000000.0
        DCVolts = ChannelValueVolts
    else:
        UPS_Error('Error_Voltage_Measurement')
    ads1256.stop()

    return DCVolts