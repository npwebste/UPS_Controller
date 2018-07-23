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
import logging

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

# Define analog input positive and negative pairs
EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM
ads = ADS1256()

def PWM_Measure_Voltage(Measurement):
    global ads
    CH_SEQ =(EXT3,EXT4)
    # Connect to ADS1256 chip
    #ads = ADS1256()

    # Calibrate gain and offset
    ads.cal_self()
    Volts = ads.read_sequence(CH_SEQ)
    # Measure DC link or solar voltage
    if Measurement == 'DC_Link':
        #adsread = ads.read_oneshot(EXT3)
        DCVolts = Volts[0] * ads.v_per_digit
    elif Measurement == 'Solar':
        #adsread = ads.read_oneshot(EXT4)
        DCVolts = Volts[1] * ads.v_per_digit
    else:
        logger.info('Error reading voltage measurement')

    return DCVolts