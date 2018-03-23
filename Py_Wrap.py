from ctypes import *

import time

#load the shared object file
adder = CDLL('./VFD_C.so')

HB =1
LB =13

xHB = hex(HB)
xLB = hex(LB)

B = xHB+xLB

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
