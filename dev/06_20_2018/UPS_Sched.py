def PWM_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, PWM_Thread, (scheduler, interval, action, actionargs))
    temp2 = action(actionargs)
    return temp2

def Protection_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, Protection_Thread, (scheduler, interval, action, actionargs))
    action()

def VFD_Thread(scheduler, interval, action, actionarg1=(),actionarg2=()):
    scheduler.enter(interval, 1, VFD_Thread, (scheduler, interval, action, actionarg1,actionarg2))
    action(actionarg1,actionarg2)

def SCIP_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, SCIP_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)

def SQL_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, SQL_Thread, (scheduler, interval, action, actionargs))
    action()