# -*- coding: utf-8 -*-
"""LP TFM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1deSddfy9aj2hLGOwizd98Yfl4OTZqumL
"""

!pip install pulp
!apt-get install -y -qq glpk-utils

# Commented out IPython magic to ensure Python compatibility.
# % pip install pulp            # PuLP
# % apt-get install glpk-utils  # GLPK

from pulp import *

import pandas as pd 
import numpy as np

prob = LpProblem('TFM_Ana', LpMaximize)

country = pd.read_csv('/content/novotfmvino-correlación - Hoja 1 (1).csv', decimal=',')

country = country.drop(['u3', 'x3','x11', 'País'],axis=1)
country

variables = list(country)

cantidad = dict(zip(variables, country['u2'+'u1']))

costs = dict(zip(variables, country['x5'+'x1']))

distancia = dict(zip(variables, country['x10'+'x9']))

total = LpVariable.dicts("total",country,lowBound=0,cat='Continuous')

prob += lpSum([cantidad[i]*total[i] for i in variables])

prob += lpSum([cantidad[f] * total[f] for f in total]) >= 0
prob += lpSum([cantidad[f] * total[f] for f in total]) <= 100000000

prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)

obj = value(prob.objective)
print("resultado: ${}".format(round(obj,2)))

for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)

"""https://towardsdatascience.com/linear-programming-and-discrete-optimization-with-python-using-pulp-449f3c5f6e99"""

2x + y <= 100
  x + y <= 80
  x <=40

from pulp import *

x = LpVariable("x1", 0, 40)   # 0<= x <= 40
y = LpVariable("x2", 0, 1000) # 0<= y <= 1000

prob = LpProblem("problem", LpMaximize)

prob += 2*x + y <= 100 
prob += x + y <= 80

prob += 3*x+2*y

status = prob.solve(GLPK(msg=0))
LpStatus[status]

value(x)

value(y)