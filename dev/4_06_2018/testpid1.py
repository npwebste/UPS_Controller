#!/usr/bin/python
import PID
import time

def test_pid(P = 0.1,  I = 0.0, D= 0.0, L=100):
    pid = PID.PID(P, I, D)

    pid.SetPoint=0.0
    #pid.setSampleTime(0.01)

    END = L
    feedback = 325
    Vin = 250
    D = .5

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        r = output = pid.output
        print('PID Output = ',r)
        D += output
        if (D >.9):
            D = .9
        elif (D < 0):
            D = 0.01
        print('D =',D)
        pid.SetPoint = 350
        time.sleep(0.02)
        print(feedback)
        feedback += 1
        #feedback += (output - (1/i))
        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)

if __name__ == "__main__":
    test_pid(.005, 0, 0, L=2000)
#    test_pid(0.8, L=50)
