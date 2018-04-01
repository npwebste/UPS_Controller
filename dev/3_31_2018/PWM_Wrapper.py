from ctypes import *

import time

#load the shared object file
PWM_C = CDLL('./PWM_C_C.so')


class PWM:
	
	def PWM_Setup():
		Setup = PWM_C.wiringPiSetup()
		return
	
	def PWM_Pin_Mode(Pin,Output):
		Pin_Mode = PWM_C.PWM_Pin_Mode(Pin,Output)
		return Pin_Mode

	def PWM_Set_Mode(Mode):
		Set_Mode = PWM_C.PWM_Pin_Mode(Mode)
		return Set_Mode
	
	def PWM_Set_Clock(Divisor):
		Set_Clock = PWM_C.PWM_Set_Clock(Divisor)
		return Set_Clock
	
	def PWM_Set_Range(Range):
		Set_Range = PWM_C.PWM_Set_Range(Range)
		return
		
	def PWM_Write(Pin,Value):
		PWM_Write = PWM_C.PWM_Write(Pin,Value)
		return


class VFD:
	
	def VFDInit(Device, Baud, Data, Stop, ID):
		Init = VFD_C.VFDInit(Device, Baud, Data, Stop, ID)
		return Init
	
	def VFDWrite(Address,Data):
		Write = VFD_C.writeVFDRegister(Address,Data)
		return Write
	
	def VFDRead():
		Read = VFD_C.readVFDRegister(Address)
		return Read
	
	def VFDClose():
		Close = VFD_C.VFDClose
		return Close


#Find sum of integers
res_init = adder.VFDInit("/dev/ttyUSB0",9600,8,1,1)
res_writ = adder.writeVFDRegister(8192,1)
time.sleep(5)
res_writ = adder.writeVFDRegister(0269,7680)
time.sleep(5)
res_writ = adder.writeVFDRegister(0269,3840)
time.sleep(5)
res_writ = adder.writeVFDRegister(8192,3)
#res_read = adder.readVFDRegister(15)
#print "Initialization: " + str(res_init)
print "Write: " + str(res_writ)
#print "Read " + str(res_read)
res_clos = adder.VFDClose()
