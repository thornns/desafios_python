"""
Exercício - Mini Projeto de Análise de Dados
Vamos fazer um exercício completo de pandas para um miniprojeto de análise de dados.

O que temos?
Temos os dados de 2019 de uma empresa de prestação de serviços.

CadastroFuncionarios
CadastroClientes
BaseServiçosPrestados

Obs: Lembrando as opções mais usuais de encoding:
encoding='latin1', encoding='ISO-8859-1', encoding='utf-8' ou então encoding='cp1252'

Observação Importante: Se o seu código der um erro na hora de importar os arquivos:

CadastroClientes.csv
CadastroFuncionarios.csv
Use separador ";" (ponto e vírgula) para resolver
"""
import pandas as pd

clientes = pd.read_csv(r'CadastroClientes.csv', sep=';')
funcionarios = pd.read_csv(r'CadastroFuncionarios.csv', sep=';', decimal=',')
funcionarios.drop(['Cargo', 'Estado Civil'], axis=1)
servicos = pd.read_excel(r'BaseServiçosPrestados.xlsx')

"""
Qual foi o gasto total com salários de funcionários pela empresa?
"""

gasto_total_salarios = funcionarios['Salario Base'].sum() +\
                       funcionarios['Impostos'].sum() +\
                       funcionarios['Beneficios'].sum() +\
                       funcionarios['VT'].sum() +\
                       funcionarios['VR'].sum()
print("Valor total gasto com salários: {:,.2f}".format(gasto_total_salarios))

"""
Qual foi o faturamento da empresa?
"""

faturamento = servicos.merge(clientes, on='ID Cliente')
faturamento['Faturamento Total'] = faturamento['Tempo Total de Contrato (Meses)'] * faturamento['Valor Contrato Mensal']

print("Faturamento total: {:,}".format(faturamento['Faturamento Total'].sum()))

"""
Qual o % de funcionários que já fechou algum contrato?
"""

fechou_contrato = len(servicos['ID Funcionário'].unique()) / len(funcionarios['ID Funcionário'])
print("Funcionários que fecharam contrato (%): {:.2%}".format(fechou_contrato))

"""
Calcule o total de contratos que cada área da empresa já fechou
"""

contratos_area = servicos.merge(funcionarios, on='ID Funcionário')
print("Total de contratos por área:\n{}".format(contratos_area['Area'].value_counts()))


"""
Calcule o total de funcionários por área
"""

print("Funcionários por Área:\n{}".format(funcionarios['Area'].value_counts()))

"""
Qual o ticket médio mensal (faturamento médio mensal) dos contratos?
"""

valor_medio = clientes['Valor Contrato Mensal'].mean()
print("Valor do ticket médio: {:.2f}".format(valor_medio))
