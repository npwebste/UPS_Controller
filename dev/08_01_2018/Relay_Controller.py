# ©2018 The Arizona Board of Regents for and on behalf of Arizona State University and the Laboratory for Energy And Power Solutions, All Rights Reserved.
#
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
from PWM_Wrapper import *
import Parameters
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

# Transfer switch function to switch between solar and grid power source
def Transfer_Switch(Relay_State):
    if Relay_State == 1:
        PWM.Digital_Write(Parameters.AC_DigitalPin,1) # Set solar power source
        logger.info('Transfer relay set to solar power source')
    elif Relay_State == 0:
        PWM.Digital_Write(Parameters.AC_DigitalPin,0) # Set grid power source
        logger.info('Transfer relay set to grid power source')
    else:
        logger.error('Invalid transfer switch command')

def DC_Relay(Relay_State):
    if Relay_State == 1:
        PWM.Digital_Write(Parameters.DC_DigitalPin, 1)  # Set solar relay in closed position
        logger.info('Solar PV DC relay set to closed position')
    elif Relay_State ==0:
        PWM.Digital_Write(Parameters.DC_DigitalPin, 0)  # Set solar relay in open position
        logger.info('Solar PV DC relay set to open position')
    else:
        logger.error('Invalid DC relay command')