from ctypes import *

#load the shared object file
adder = CDLL('./CLibModbus.so')

#Find sum of integers
ret_init = CLibModbus.VFDInit("/dev/ttyUSB0",9600,'N',8,1,1)
ret_writ = CLibModbus.writeVFDRegister(2000,0001)
print "Initialization: " + str(res_init)
print "Write: " + str(res_writ)