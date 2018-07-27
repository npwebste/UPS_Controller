# ©2018 The Arizona Board of Regents for and on behalf of Arizona State University and the Laboratory for Energy And Power Solutions, All Rights Reserved.
#
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