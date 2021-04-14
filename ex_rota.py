import pandas as pd, numpy as np
from ortools.sat.python import cp_model

#entrada
nos = pd.read_excel('rotas_input.xlsx', sheet_name='nos')
caminhos = pd.read_excel('rotas_input.xlsx', sheet_name='caminhos')
n_nos = len(nos)
n_caminhos = len(caminhos)

#modelo
model = cp_model.CpModel()
x = np.zeros(n_caminhos).tolist()
for c in caminhos.index:
    x[c] = model.NewIntVar(0,1, 'x[{}]'.format([c]))

#função objetivo
model.Minimize(sum([x[c] * caminhos.distancia[c] for c in caminhos.index]))

#restrições
no_origem = int(nos.no[nos.desc=='origem'])
no_destino = int(nos.no[nos.desc=='destino'])
model.Add(sum([x[c] for c in caminhos.index[caminhos.no_de==no_origem]])==1)
model.Add(sum([x[c] for c in caminhos.index[caminhos.no_para==no_destino]])==1)

for no in nos.no[nos.desc=='meio']:
    sum_entra = sum([x[c] for c in caminhos.index[caminhos.no_para==no]])
    sum_sai = sum([x[c] for c in caminhos.index[caminhos.no_de==no]])
    model.Add(sum_sai <= 1)
    model.Add(sum_entra <= 1)
    model.Add(sum_entra == sum_sai)
    
#resolver
solver = cp_model.CpSolver()
status = solver.Solve(model)

#imprimir
print('Status =', solver.StatusName(status))
print('FO =', solver.ObjectiveValue())

caminhos['ativado'] = 0
for c in caminhos.index:
    caminhos.ativado[c] = solver.Value(x[c])
print(caminhos)

print('Rota escolhida')
for c in caminhos.index[caminhos.ativado==1]:
    print('X%i%i - %.2f' % (caminhos.no_de[c], caminhos.no_para[c], caminhos.distancia[c]))