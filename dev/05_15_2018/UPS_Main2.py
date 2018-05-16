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
import sched,time
from UPS_Sched import *
from PWM_Controller import *
from Protection_Controller import *
from SCIP_Controller import *



import Parameters
from Initialization import *
import time
import sqlite3
from VFD_Modbus_Wrapper import *
#import VFD_Modbus_Registers
from PWM_Wrapper import *
from TransferSwitch import *
from DC_PID import *
#import ads1256

global dutyold
dutyold = .5
# Declare Variables

s = sched.scheduler(time.time, time.sleep)
# Main UPS Loop
while True:
	
	# Set parametersrameters and declare variables

	# Run initializtaion to setup VFD and converter controls
	Run_Initialization()
	# UPS Control Loop
	
	
	
while True:
		
		
		PWM_Thread(s,1,PWM_Controller,)
	
	    Protection_Thread(s,Protection_Controller,)
	
    	VFD_Thread(s,VFD_Controller, )
	
	    SCIP_Thread(s,SCIP_Controller,)
	
    	SQL_Thread(s,SQL_Database,)
		
		s.run()
		
		
		#48-96
		# Vo = Vin*(1/(1-D))
		# Vo = Vin/D
		D = .6
		Val = 96*(1-D)
		#PWM.PWM_Write(Parameters.Pin,int(Val))
		#print(Parameters.Pin)
		#time.sleep(5)
		
		Transfer_Switch(1)
		print('Switch on')
		time.sleep(5)
		
		Transfer_Switch(0)
		print('Switch off')
		#d = DC_PID_Set(.0001,0,0,350,325,dutyold)
		time.sleep(5)		
		#print('From PID:',d)
		#dutyold = d
		
		#TankCheck()
		'''
		#SolarMeasured()
		#time.sleep(5)
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Frequency_Set"),1)
		time.sleep(10)
		t= VFD.VFDRead(269)
		print('Frequency is',t/100,'Hz')
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Frequency_Set"),3)
		time.sleep(15)
		'''
		'''
		if P_Solar_Measured > P_Solar_Max*P_Min_Percent:
			setPWM()
			
			if startVFD() != 0:
				startVFD()
		
			setVFD()
			
			
		else
			setGrid()
			
			if startVFD() != 0:
				startVFD()
		
			setVFD()
		'''

		#ProtectionCheck()
	

### SQL STUFF
#conn = sqlite3.connect('example.db')

#c = conn.cursor()

#c.execute('''CREATE TABLE Power(Date text, Voltage real, Current real, Power real)''')

#c.execute("INSERT INTO Power VALUES('2017',100,25,2500)")

#conn.commit()
#conn.close()