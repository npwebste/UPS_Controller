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
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from ADS1256_definitions import *
from pipyadc import ADS1256
import sqlite3
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

def Run_Initialization():
    logger.info('UPS initialization beginning')
    # Water

    # Solar

    # VFD Connection Initialization
    # VFD.VFDInit("/dev/ttyAMA0".encode('ascii'),9600,8,1,1)
    VFD.VFDInit(Parameters.Device.encode('ascii'),Parameters.Baud,Parameters.Data,Parameters.Stop,Parameters.ID)
    VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Set"),Parameters.VFD_Freq_Init) # Set initial frequency
    VFD.VFDWrite(reg.get("WriteFunc", {}).get("Frequency_Acc"),Parameters.VFD_Acc_Rate )  # Set acceleration rate

    # PWM Setup
    PWM.PWM_Setup()
    PWM.PWM_Pin_Mode(Parameters.PWMPin)
    PWM.PWM_Set_Mode()
    PWM.PWM_Set_Clock(Parameters.Divisor)
    PWM.Pin_Mode_Output(Parameters.AC_DigitalPin)
    PWM.Pin_Mode_Output(Parameters.DC_DigitalPin)
    PWM.PWM_Set_Range(Parameters.Range)
    PWM.PWM_Write(Parameters.PWMPin, int(Parameters.PID_OLD_INIT*Parameters.Range))

    # SQL Database Setup
    try:
        conn = sqlite3.connect('UPS_DB.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE UPS_DB(Date text,Solar_Voltage real, DC_Link_Voltage real, Duty_Cycle real, VFD_Freq real, VFD_Volt real, VFD_Amps real, VFD_Power real, Grid_Power real, Solar_Power real, VFD_BusVolt real, VFD_Temp real)''')
        conn.commit()
        logger.info('SQL Database Created')
    except:
        conn.rollback()
        logger.info('SQL Database Already Created')
    finally:
        conn.close()
        logger.info('SQL Database Closed')

    logger.info('UPS initialization complete')