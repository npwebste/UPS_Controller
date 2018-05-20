def PWM_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, PWM_Thread, (scheduler, interval, action, actionargs))
    print(action(actionargs))


def Protection_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, Protection_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)


def VFD_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, VFD_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)


def SCIP_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, SCIP_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)


def SQL_Thread(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, SQL_Thread, (scheduler, interval, action, actionargs))
    action(actionargs)
