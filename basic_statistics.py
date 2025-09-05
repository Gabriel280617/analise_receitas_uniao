import pandas as pd

import pandasgui
from pandas.conftest import axis_1

df = pd.read_csv('Receita-Orcamentaria-da-Uniao.csv', encoding='latin1', sep=';')


colunas = [
    'ANO DE REFERENCIA', 'RECEITAS CORRENTES', 'RECEITA TRIBUTARIA',
    'RECEITA DE CONTRIBUICOES', 'RECEITA PATRIMONIAL', 'RECEITA AGROPECUARIA',
    'RECEITA INDUSTRIAL', 'RECEITA DE SERVICOS', 'TRANSFERENCIA CORRENTES',
    'OUTRAS RECEITAS CORRENTES', 'RECEITAS DE CAPITAL', 'OPERACOES DE CREDITO'
]

def formatar_valor(valor):
    if valor >= 1e12:  # Trilhões
        return f'R$ {valor / 1e12:,.2f}T'
    elif valor >= 1e9:  # Bilhões
        return f'R$ {valor / 1e9:,.2f}B'
    elif valor >= 1e6:  # Milhões
        return f'R$ {valor / 1e6:,.2f}M'
    else:
        return f'R$ {valor:,.2f}'

df = df[colunas]

#Cleaning
for col in df.columns[1:]:
    df[col] = df[col].replace('[.,]', '', regex=True).astype(float, errors='ignore') / 100
df.fillna(0, inplace=True)


#Create a new dataset with basic statistics
df_statistic = df.describe()
df_statistic = df_statistic.drop('ANO DE REFERENCIA', axis=1)

#format the value for better understanding
for col in df_statistic.columns:
    df_statistic[col] = df_statistic[col].apply(formatar_valor)

#show on screen with pandasgui
pandasgui.show(df_statistic)


