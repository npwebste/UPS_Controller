def PWM_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, PWM_Thread, (scheduler, interval, action, actionargs))
    D_temp2 = action(actionargs)
    print("PWM")
    return D_temp2

def Protection_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 2, Protection_Thread, (scheduler, interval, action, actionargs))
    action()
    print("Protection")

def VFD_Thread(scheduler, interval, action, actionarg1=(),actionarg2=()):
    scheduler.enter(interval, 1, VFD_Thread, (scheduler, interval, action, actionarg1,actionarg2))
    action(actionarg1,actionarg2)
    print("VFD")

def SCIP_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, SCIP_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)

def SQL_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 3, SQL_Thread, (scheduler, interval, action, actionargs))
    action()
    print("SQL")