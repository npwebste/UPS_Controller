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
import Parameters
import sqlite3
import sched
import time
import logging
import PWM_Controller
import VFD_Controller
from datetime import datetime
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from Relay_Controller import *

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

def SQL_Database_Controller_Main(arg):

    # Setup SQL scheduler
    SQL_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the SQL controller and run
        SQL_Sched.enter(Parameters.SQL_Database_Controller_Interval, 1, SQL_Database_Controller, ("",))
        SQL_Sched.run()

def SQL_Database_Controller(arg):
    Solar_Voltage = PWM_Controller.Solar_Actual_Volts
    DC_Link_Voltage = PWM_Controller.DC_Link_Actual_Volts
    Duty_Cycle = PWM_Controller.D_PID_OLD
    VFD_Freq = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Frequency")) / 100
    VFD_Volt = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Voltage"))
    VFD_Amps = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Current")) / 100
    VFD_Power = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Power"))*100
    VFD_BusVolt = VFD.VFDRead(reg.get("ReadFunc", {}).get("Bus_Voltage"))
    VFD_Temp = VFD.VFDRead(reg.get("ReadFunc", {}).get("Temperature"))

    if VFD_Controller.Solar_State ==1:
        Solar_Power = VFD_Power
        Grid_Power = 0
    elif VFD_Controller.Grid_State == 1:
        Solar_Power = 0
        Grid_Power = VFD_Power
    else:
        Solar_Power = 0
        Grid_Power = 0

    Currenttime = datetime.now()
    try:
        conn = sqlite3.connect('UPS_DB.db')
        c = conn.cursor()
        c.execute("INSERT INTO UPS_DB(Date,Solar_Voltage, DC_Link_Voltage, Duty_Cycle, VFD_Freq, VFD_Volt, VFD_Amps, VFD_Power, Grid_Power, Solar_Power, VFD_BusVolt, VFD_Temp) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(Currenttime, Solar_Voltage,DC_Link_Voltage, Duty_Cycle,VFD_Freq,VFD_Volt,VFD_Amps,VFD_Power, Grid_Power, Solar_Power, VFD_BusVolt,VFD_Temp))
        conn.commit()

    except:
        conn.rollback()
        logger.error('Could not connect and write to SQL database')
    conn.close()