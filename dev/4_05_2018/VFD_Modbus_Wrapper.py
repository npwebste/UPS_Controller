from ctypes import *

#Load the shared object file
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