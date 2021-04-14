import pandas as pd
dados_pessoas = pd.read_excel('dados.xlsx', sheet_name='pessoas')
dados_notas = pd.read_excel('dados.xlsx', sheet_name='notas')

dados_todos = dados_notas.set_index('nome').join(dados_pessoas.set_index('nome'))

medias = dados_todos.groupby('nome').nota.mean()

medias.to_excel('saida.xlsx')