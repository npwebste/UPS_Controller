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
from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
import sqlite3
import Parameters
#USB0
def Run_Initialization():
	
	# Water
	
	# Solar
	
	
	# VFD
	#VFD.VFDInit("/dev/ttyAMA0".encode('ascii'),9600,8,1,1)
	VFD.VFDInit(Parameters.Device.encode('ascii'),Parameters.Baud,Parameters.Data,Parameters.Stop,Parameters.ID)

	# PWM
	PWM.PWM_Setup()
	PWM.PWM_Pin_Mode(Parameters.Pin)
	PWM.PWM_Set_Mode()
	PWM.PWM_Set_Clock(Parameters.Divisor)
	PWM.Pin_Mode_Output(6)
	PWM.PWM_Set_Range(Parameters.Range)

	conn = sqlite3.connect('UPS_DB.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE UPS_DB(Date text,Solar_Voltage real, DC_Link_Voltage real, VFD_Freq real, VFD_Volt real, VFD_Amps real, VFD_Power real, VFD_BusVolt real, VFD_Temp real)''')
	conn.commit()
	conn.close()
