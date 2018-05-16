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

from VFD_Modbus_Wrapper import *
from VFD_Modbus_Registers import *
from PWM_Wrapper import *
from TransferSwitch import *

def VFD_Controller(Solar_Power):
	file
	





# Main UPS Loop
while True:
	
	# Set parametersrameters and declare variables
	# Run initializtaion to setup VFD and converter controls
	Run_Initialization()

	# UPS Control Loop
	while True:
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Motor_Start_Stop"),1)
		time.sleep(7)
		
		Freq = input('Enter frequency setpoint: ')
		print('Setting frequency to: ', int(float(Freq)*100))
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Frequency_Set"),int(float(Freq)*100))
		time.sleep(7)	
		
		t= VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Frequency"))
		print('Frequency is',t/100,'Hz')
		
		t1 = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Voltage"))
		print('Voltage is',t1,'V')
		
		t2 = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Current"))
		print('Current is',t2/100,'A')
		
		t3 = VFD.VFDRead(reg.get("ReadFunc",{}).get("Output_Power"))
		print('Power is',t3/10,'W')
		
		t4 = VFD.VFDRead(reg.get("ReadFunc",{}).get("Bus_Voltage"))
		print('Bus Voltage is',t4,'V')
		time.sleep(10)
		
		VFD.VFDWrite(reg.get("WriteFunc",{}).get("Motor_Start_Stop"),3)
		time.sleep(15)