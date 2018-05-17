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
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from TransferSwitch import *

def SQL_Database(Solar_Power):
    Solar_Voltage = PWM_Measure_Voltage('Solar')
    DC_Link_Voltage = PWM_Measure_Voltage('DC_Link')
    VFD_Freq = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Frequency")) / 100
    VFD_Volt = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Voltage"))
    VFD_Amps = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Current")) / 100
    VFD_Power = VFD.VFDRead(reg.get("ReadFunc", {}).get("Output_Power")) / 10
    VFD_BusVolt = VFD.VFDRead(reg.get("ReadFunc", {}).get("Bus_Voltage"))
    VFD_Temp = VFD.VFDRead(reg.get("ReadFunc", {}).get("Temperature"))

    conn = sqlite3.connect('UPS_DB.db')
    c = conn.cursor()

    c.execute("INSERT INTO UPS_DB VALUES(Solar_Voltage,DC_Link_Voltage,VFD_Freq,VFD_Volt,VFD_Volt,VFD_Amps,VFD_Power,VFD_BusVolt,VFD_Temp)")

    conn.commit()

    conn.close()

### SQL STUFF
#conn = sqlite3.connect('example.db')

#c = conn.cursor()

#c.execute('''CREATE TABLE Power(Date text, Voltage real, Current real, Power real)''')

#c.execute("INSERT INTO Power VALUES(',100,25,2500)")

#conn.commit()
#conn.close()