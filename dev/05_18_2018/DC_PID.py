#!/usr/bin/python
import PID
import time
import Parameters

def DC_PID_Set(P, I, D, DC_Setpoint, DC_Measurement,DutyOld):
    pid = PID.PID(P, I, D)

    pid.SetPoint=DC_Setpoint
    Duty = DutyOld
    pid.update(DC_Measurement)
    output = pid.output
    round_output = round(output)
    print('PID Output = ',output)
    Duty += output
    if (Duty >.9):
        Duty = .9
    elif (Duty < .1):
        Duty = 0.1
    print('Duty =',D)
	
    return Duty