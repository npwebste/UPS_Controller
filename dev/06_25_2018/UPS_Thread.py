from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import Parameters
import sys

def PWM_Thread(scheduler, interval, action, actionargs=()):
    #print("Value=",actionargs)
    D_temp2 = action(actionargs)
    scheduler.enter(interval, 1, PWM_Thread, (scheduler, interval, action, D_temp2))
    #D_temp2 = multithreading(action,'actionargs',1)
    print("PWM")
    #print("D_Temp2 =",D_temp2)
    return D_temp2

def Protection_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 2, Protection_Thread, (scheduler, interval, action, actionargs))
    action()
    #multithreading(action(),(),4)
    print("Protection")

def VFD_Thread(scheduler, interval, action, actionarg1=(),actionarg2=()):
    scheduler.enter(interval, 1, VFD_Thread, (scheduler, interval, action, actionarg1,actionarg2))
    action(actionarg1,actionarg2)
    #multiprocessing(action,(actionarg1,actionarg2),4)
    print("VFD")

def SCIP_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, SCIP_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)

def SQL_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 3, SQL_Thread, (scheduler, interval, action, actionargs))
    action()
    print("SQL")


def multithreading(func, args, workers):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, args)
    return res


def multiprocessing(func, args, workers):
    with ProcessPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, args)
    return res