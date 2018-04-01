from ctypes import *

import time

#load the shared object file
VFD_C = CDLL('./VFD_C.so')

class VFD:
	
	def VFDInit(Device, Baud, Data, Stop, ID):
		Init = VFD_C.VFDInit(Device, Baud, Data, Stop, ID)
		return Init
	
	def VFDWrite(Address,Data):
		Write = VFD_C.writeVFDRegister(Address,Data)
		return Write
	
	def VFDRead(Address):
		Read = VFD_C.readVFDRegister(Address)
		return Read
	
	def VFDClose():
		Close = VFD_C.VFDClose
		return Close
	def SetResponse(sec,usec):
                SetResp = VFD_C.SetResponseTimeoutVFD(sec,usec)
                return SetResp
"""
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
"""