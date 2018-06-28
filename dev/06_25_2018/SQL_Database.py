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
import Parameters
import sqlite3
import sched
import time
from datetime import datetime
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Measure_Voltage import *
from PWM_Wrapper import *
from TransferSwitch import *

SQL_Sched = sched.scheduler(time.time,time.sleep)

def SQL_Database(arg):
    Solar_Voltage = PWM_Measure_Voltage('Solar')/Parameters.Voltage_Multiplier
    DC_Link_Voltage = PWM_Measure_Voltage('DC_Link')/Parameters.Voltage_Multiplier
    VFD_Freq = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Frequency")) / 100
    VFD_Volt = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Voltage"))
    VFD_Amps = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Current")) / 100
    VFD_Power = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Power")) / 10
    VFD_BusVolt = VFD.VFDRead(reg.get("ReadFunc", {}).get("Bus_Voltage"))
    VFD_Temp = VFD.VFDRead(reg.get("ReadFunc", {}).get("Temperature"))
    Currenttime = datetime.now()
    try:
        conn = sqlite3.connect('UPS_DB.db')
        c = conn.cursor()
        c.execute("INSERT INTO UPS_DB(Date,Solar_Voltage, DC_Link_Voltage, VFD_Freq, VFD_Volt, VFD_Amps, VFD_Power, VFD_BusVolt, VFD_Temp) VALUES(?,?,?,?,?,?,?,?,?)",(Currenttime, Solar_Voltage,DC_Link_Voltage,VFD_Freq,VFD_Volt,VFD_Amps,VFD_Power,VFD_BusVolt,VFD_Temp))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("SQL write failed")
        raise e
    conn.close()

    SQL_Sched.enter(5,1,SQL_Database,("",))
    SQL_Sched.run()