from Feedback import *
from PWM_PID import *
from PWM_Wrapper import *
import time

PWM.PWM_Setup()
PWM.PWM_Pin_Mode(Parameters.PWMPin)
PWM.PWM_Set_Mode()
PWM.PWM_Set_Clock(Parameters.Divisor)
PWM.PWM_Set_Range(Parameters.Range)
D_PID_OLD = .5
while 1:
    VM = do_measurement()
    print("Voltage Measurement=",VM)
    #time.sleep(1)
    Actual = VM/Parameters.Voltage_Multiplier
    #Actual = int(round(VM/Parameters.Voltage_Multiplier,1))
    print("Actual Voltage=",Actual)
    D_PID = PWM_PID(Actual,D_PID_OLD)
    D_PID_OLD = D_PID
    print("Duty Cycle=",D_PID)
    #time.sleep(1)
    Convert = int(round(D_PID*96,0))
    #print(Convert)
    PWM.PWM_Write(Parameters.PWMPin,Convert)