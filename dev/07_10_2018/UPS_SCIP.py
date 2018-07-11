# Universal Power System Controller
# USAID Middle East Water Security Initiative
#
# Developed by: Nathan Webster
# Primary Investigator: Nathan Johnson
#
# Version History (mm_dd_yyyy)
# 1.00 07_13_2018_NW
#
######################################################

from pyscipopt import Model, quicksum

#Initialize model
model = Model("UPS_Controller")

time = [0, 1]

Solar_Forecast = [100,1000]
Water_Forecast = [.004,.008]
P_Grid = 2000
Theta_Max = 314
eta = 1

Ap = .000127
As = 1.12
Am = 15.6
Km = .0000000064
Vp = .00002075/6.28
rho = 1007
P_Osmotic = 377490

s_opt = 1
hmax = 1.2

def UPS_SCIP_Call():
    # Create variables
    P_Solar_Ref, P_In_G, P_In_S, P_RO, st, Fp, Yopt, P_Sys, Vf, hdot, h, Theta_VFD, Vr, Alpha, Obj1, Obj2, Obj3, Obj4 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

    for t in time:
        P_Solar_Ref[t] = model.addVar(vtype="I", name="Solar Reference(%s)" % t)
        P_In_G[t] = model.addVar(vtype="C", name="Grid Power(%s)" % t)
        P_In_S[t] = model.addVar(vtype="C", name="Solar Power(%s)" % t)
        P_RO[t] = model.addVar(vtype="C", name="RO Power(%s)" % t, lb=0, ub=2000)
        st[t] = model.addVar(vtype="C", name="Tank Level(%s)" % t, ub=1)
        Fp[t] = model.addVar(vtype="C", name="Inlet Flow Rate(%s)" % t, lb=0, ub=4)
        Yopt[t] = model.addVar(vtype="C", name="Optimal Recovery(%s)" % t, lb=.6, ub=1)
        P_Sys[t] = model.addVar(vtype="C", name="Pressure(%s)" % t)
        Vf[t] = model.addVar(vtype="C", name="Clean Flow Rate(%s)" % t)
        hdot[t] = model.addVar(vtype="C", name="Change In Tank Height(%s)" % t)
        h[t] = model.addVar(vtype="C", name="Tank Height(%s)" % t, lb=0, ub=hmax)
        Theta_VFD[t] = model.addVar(vtype="C", name="Frequency(%s)" % t, lb=0, ub=Theta_Max)
        Vr[t] = model.addVar(vtype="C", name="Reject Flow Rate(%s)" % t, lb=0, ub=2)

        Obj1[t] = model.addVar(vtype="C", name="Obj1 (%s)" % t)
        Obj2[t] = model.addVar(vtype="C", name="Obj2 (%s)" % t)
        Obj3[t] = model.addVar(vtype="C", name="Obj3 (%s)" % t)
        Obj4[t] = model.addVar(vtype="C", name="Obj4 (%s)" % t)

        Alpha[t] = model.addVar(vtype="B", name='Binary Var (%s)' % t)

    # Create Constraints

    for t in time:
        model.addCons(P_RO[t] == ((Alpha[t] * P_In_G[t]) + ((1 - Alpha[t]) * P_In_S[t])), name="Power Balance")

        model.addCons(0 <= (P_Solar_Ref[t] <= Solar_Forecast[t]), name="SolarMax (%s)" % t)

        model.addCons(P_In_G[t] == ((Theta_VFD[t] / Theta_Max) * (Alpha[t] * P_Grid)), name="Grid Power Equality")

        model.addCons(P_In_S[t] == ((Theta_VFD[t] / Theta_Max) * ((1 - Alpha[t]) * P_Solar_Ref[t])),
                      name="Solar Power Equality")

        model.addCons(P_Sys[t] == (((rho * Ap) / (Am * Km)) * (Vf[t] - Vr[t])) + P_Osmotic,
                      name="System Pressure Equality")

        model.addCons(Fp[t] == ((Vf[t] - Vr[t]) * Ap), name="Flow")

        model.addCons(Yopt[t] == ((Vf[t] - Vr[t]) / Vf[t]), name="Optimal Recovery")

        model.addCons(hdot[t] == ((Ap / As) * (Vf[t] - Vr[t])) - (Water_Forecast[t] / As), name="Change Tank Level")

        # model.addCons(h[t] == h[t]+hdot[t], name="Tank Level Update")

        model.addCons(st[t] == h[t] / hmax, name="Tank Percentage")

        model.addCons(Vf[t] == (Theta_VFD[t] * Vp) / Ap, name="Flow Rate Calc")

        model.addCons(P_RO[t] == (1 / eta) * ((P_Sys[t] * Fp[t] / Yopt[t]) + .5 * (
                    (Fp[t] * Fp[t] * Fp[t]) / ((Yopt[t] * Yopt[t] * Yopt[t]) * (Ap * Ap))) * rho), name="RO Power Calc")

        model.addCons(Obj1[t] == abs((P_RO[t] - P_In_G[t])), name="Obj1")

        model.addCons(Obj2[t] == abs((P_RO[t] - P_In_S[t])), name="Obj2")

        model.addCons(Obj3[t] == abs((st[t] - s_opt)), name="Obj3")

        model.addCons(Obj4[t] == P_RO[t] / Fp[t], name="Obj4")

    for t in time:
        if t < 23:
            model.addCons(h[t+1] == h[t] + hdot[t], name="Tank Level Update")
    model.setObjective(quicksum((Obj1[t] + Obj2[t] + Obj3[t] + Obj4[t]) for t in time), "minimize")
    model.optimize()
    print(model.getStatus())
    print
    "Objective value: ", model.getObjVal()


for t in time:
    print "Solar Power(%s) = "  %t, model.getVal(P_In_S[t])
    print "Grid Power(%s) = " %t, model.getVal(P_In_G[t])
    print "RO Power(%s) = " %t, model.getVal(P_RO[t])