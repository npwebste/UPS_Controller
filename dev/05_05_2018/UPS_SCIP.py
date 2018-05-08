from pyscipopt import Model, quicksum

#Initialize model
model = Model("UPS_Controller")

Solar_Forecast = [500,1000]
Water_Forecast = [1,1.5]
P_Grid = 2500
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

weight1 = .01
weight2 = .01
weight3 = .001
weight4 = .01

# Create variables
P_Solar_Ref, P_In_G, P_In_S, P_RO, st, Fp, Yopt, P_Sys, Vf, hdot, h, Theta_VFD, Vr = {}

for t in time:
	P_Solar_Ref[t] = model.addVar(vtype="C", name="Solar Reference(%s)"%j)
	P_In_G[t] = model.addVar(vtype="C", name="Grid Power(%s)"%j)
	P_In_S[t] = model.addVar(vtype="C", name="Solar Power(%s)"%j)
	P_RO[t] = model.addVar(vtype="C", name="RO Power(%s)"%j, lb=0, ub=2500)
	st[t] = model.addVar(vtype="C", name="Tank Level(%s)"%j, ub = 1)
	Fp[t] = model.addVar(vtype="C", name="Inlet Flow Rate(%s)"%j, lb=0, ub = 4)
	Yopt[t] = model.addVar(vtype="C", name="Optimal Recovery(%s)"%j, lb=.6, ub=1)
	P_Sys[t]= model.addVar(vtype="C", name="Pressure(%s)"%j)
	Vf[t] = model.addVar(vtype="C", name="Clean Flow Rate(%s)"%j)
	hdot[t]= model.addVar(vtype="C", name="Change In Tank Height(%s)"%j)
	h[t] = model.addVar(vtype="C", name="Tank Height(%s)"%j, lb=0, ub=hmax)
	Theta_VFD[t] = model.addVar(vtype="C", name="Frequency(%s)"%j, lb=0, ub=Theta_Max)
	Vr[t] = model.addVar(vtype="C", name="Reject Flow Rate(%s)"%j, lb=0, ub=2)
	
	Alpha[t] = modle.addVar(vtype="B", name='x (%s)'%j)

# Create Constraints

for t in time:
	model.addCons(P_RO[t]==((Alpha[t]*P_In_G[t])+((1-Alpha[t])*P_In_S[t])), name="Power Balance")

	model.addCons(P_Solar_Ref[t]>=0)

	model.addCons(P_Solar_Ref[t]<=max(Solar_Forecast[t]))
	
model.setObjective(quicksum(abs(P_RO[t]-P_In_G[t]) for t in time),"minimize")

model.optimize

if model.getStatus() == "optimal":
    print("Optimal value:", model.getObjVal())

    for t in time:
        print(P_In_G[t].name, "=", model.getVal(P_In_G[t]))
else:
    print("Problem could not be solved to optimality")
'''
# Create constraints
c = {}
for i in Grapes:
    c[i] = model.addCons(quicksum(Use[i,j]*x[j] for j in Blends) <= Inventory[i], name="Use(%s)"%i)

# Objective
model.setObjective(quicksum(Profit[j]*x[j] for j in Blends), "maximize")


# Objective
minimize cost : weight1*sum{t in DATA} (((P_RO[t]-P_In_G[t])^2))+weight2*sum{t in DATA} (((P_RO[t]-P_In_S[t])^2))+weight3*sum{t in DATA} (st[t]-sopt)^2 +weight4*sum{t in DATA} ((P_RO[t]/Fp[t]));

# Constraints


subject to Power_G {t in DATA}:
P_In_G[t] = (Theta_VFD[t]/Theta_Max)*((Alpha)*P_Grid);

subject to Power_S {t in DATA}:
P_In_S[t] = (Theta_VFD[t]/Theta_Max)*((1-Alpha)*P_Solar_Ref[t]);

subject to water1 {t in DATA}:
P_Sys[t] = (((rho*Ap)/(Am*Km))*(Vf[t]-Vr[t]))+P_Osmotic;

subject to Fp3 {t in DATA}:
Fp[t] = (Vf[t]-Vr[t])*Ap;


subject to Yopt3 {t in DATA}:
Yopt[t] = (Vf[t]-Vr[t])/Vf[t];

subject to xdot {t in DATA}:
hdot[t]=((Ap/As)*(Vf[t]-Vr[t]))-(Water_Forecast[t]/As);

subject to xdot1 {t in DATA: t>=2}:
h[t] = h[t-1]+hdot[t];



subject to slevel {t in DATA}:
st[t] = h[t]/hmax;


subject to water4 {t in DATA}:
Vf[t] = (Theta_VFD[t]*Vp)/Ap;

subject to P_RO_Val {t in DATA}:
P_RO[t] = (1/eta)*((P_Sys[t]*Fp[t]/Yopt[t])+.5*(Fp[t]^3/(Yopt[t]^3*Ap^2))*rho);
'''