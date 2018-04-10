#!/usr/bin/python
import PID
import time

def DC_PID(P, I, D, DC_Setpoint, DC_Measurement):
    pid = PID.PID(P, I, D)

    pid.SetPoint=DC_Setpoint

    Duty = .5

    pid.update(DC_Measurement)
    output = pid.output
	round_output = round(output)
    print('PID Output = ',round_output)
    Duty += round_output
    if (Duty >.9):
		Duty = .9
    elif (Duty < .1):
		Duty = 0.1
	print('Duty =',D)
	
	return Duty