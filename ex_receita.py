import pyomo.environ as pyo, numpy as np
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.p = pyo.Var(bounds=(50,200))
model.N = pyo.Var(within=Integers, bounds=(0,None))
p = model.p
N = model.N

model.obj = pyo.Objective(expr= p*N, sense=maximize)
model.C1 = pyo.Constraint(expr= N == 1001-5*p)

opt = SolverFactory('couenne', executable='C:\\couenne\\bin\\couenne.exe')
opt.solve(model)

print('p:', np.round(pyo.value(p),2))
print('N:', np.round(pyo.value(N),2))
print('receita:', pyo.value(p)*pyo.value(N))
