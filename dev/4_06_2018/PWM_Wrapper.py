from ctypes import *

#Load the shared object file
PWM_C = CDLL('./PWM_C.so')

class PWM:
	
	def PWM_Setup():
		Setup = PWM_C.wiringPiSetup()
		#return Setup
	
	def PWM_Pin_Mode(Pin):
		Pin_Mode = PWM_C.PWM_Pin_Mode(Pin)
		return Pin_Mode
	    
	def Pin_Mode_Output(Pin):
		Pin_Mode = PWM_C.Pin_Mode_Output(Pin)
		return Pin_Mode

	def PWM_Set_Mode():
		Set_Mode = PWM_C.PWM_Set_Mode()
		return Set_Mode
	
	def PWM_Set_Clock(Divisor):
		Set_Clock = PWM_C.PWM_Set_Clock(Divisor)
		return Set_Clock
	
	def PWM_Set_Range(Range):
		Set_Range = PWM_C.PWM_Set_Range(Range)
		return Set_Range
		
	def PWM_Write(Pin,Value):
		PWM_Write = PWM_C.PWM_Write(Pin,Value)
		return PWM_Write
		
	def Digital_Write(Pin,Value):
		DigitalWrite = PWM_C.Digital_Write(Pin,Value)
		return DigitalWrite
		
		
		'''
		Rpi base = 19.2 MHz
		pwmSetClock 2 to 4095
		pwmSetRange up to 4096
		
		Clock = 2
		Range = 96
		
		pwmFrequency = 19.2E6/pwmClock/pwmRange
		
		freq = 19.2E6
		'''