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
from ADS1256_definitions import *
from pipyadc import ADS1256
from UPS_Messages import *

# Define analog input positive and negative pairs
EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

def PWM_Measure_Voltage(Measurement):
    # Connect to ADS1256 chip
    ads = ADS1256()

    # Calibrate gain and offset
    #ads.cal_self()

    # Measure DC link or solar voltage
    if Measurement == 'DC_Link':
        adsread = ads.read_oneshot(EXT3)
        DCVolts = adsread * ads.v_per_digit
    elif Measurement == 'Solar':
        adsread = ads.read_oneshot(EXT4)
        DCVolts = adsread * ads.v_per_digit
    else:
        UPS_Messages('Error_Voltage_Measurement')

    return DCVolts